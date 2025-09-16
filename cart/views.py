from django.shortcuts import render
from rest_framework.views import APIView
from .models import CartItem,Cart,Order,OrderedItem
# Create your views here.
from rest_framework import viewsets,status
from food.models import Item
from rest_framework.response import Response
from .serializers import CartSerializers,CartItemSerializers,OrderSerializers
from rest_framework.permissions import AllowAny,IsAdminUser

class MyCart(viewsets.ViewSet):
    
    def list(self,request):
  
        query = Cart.objects.filter(user = request.user).first()
        if not query:
            Response({"message":"No active cart Found."},status=404)

        serializer = CartSerializers(query)
        cart_pro = CartItem.objects.filter(cart = query)
        cart_data = serializer.data
        cart_itm_serializer = CartItemSerializers(cart_pro,many=True)
        cart_data["cartItem"]=cart_itm_serializer.data
    
        return Response(cart_data)
        





class AddToCartViewset(APIView):
  
    def post(self,request):
        product_id = request.data['id']
        item_pro = Item.objects.get(id = product_id)
        cart = Cart.objects.filter(user = request.user).first()
        cart_item = CartItem.objects.filter(cart=cart).first()
        try: 
            if cart:
                product_in_cart = CartItem.objects.filter(cart=cart,item=item_pro).first()
                if product_in_cart:
                    product_in_cart.quantity+=1
                    product_in_cart.subtotal+=product_in_cart.price
                    product_in_cart.save()
                    cart.total+=product_in_cart.price
                    cart.save()

                else:
                    CartItem.objects.create(
                        cart = cart,
                        item = item_pro,
                        price = item_pro.price,
                        quantity = 1,
                        subtotal = item_pro.price
                    )
                    cart.total += item_pro.price
                    cart.save()
            
            else:
                new_cart =Cart.objects.create(
                    user=request.user,
                    total=0
                )

                CartItem.objects.create(
                    cart = new_cart,
                    item = item_pro,
                    quantity = 1,
                    price = item_pro.price,
                    subtotal = item_pro.price,
                )
                new_cart.total+=item_pro.price
                new_cart.save()
            
            response_message = {'error':False,'message':'Product Succesfully Add','product_id':product_id}
                
        except:
            response_message = {'error':True,'message':'Product not Succesfully Add'}

        return Response(response_message)





class IncreaseCartItem(APIView):
 
    def post(self,request):
      cartIid = CartItem.objects.get(id=request.data['id'])
      cart_obj = cartIid.cart
      cartIid.quantity+=1
      cartIid.subtotal+=cartIid.price
         
      cartIid.save()
      cart_obj.total+=cartIid.price
      cart_obj.save()
      return Response({'error':False, 'message':'quantity increse'},status=200)


class DereaseCartItem(APIView):
    
     def post(self,request):
      cartIid = CartItem.objects.get(id=request.data['id'])
      cart_obj = cartIid.cart
      if(cartIid.quantity > 1):
            cartIid.quantity-=1
            cartIid.subtotal-=cartIid.price
            
            cartIid.save()
            cart_obj.total-=cartIid.price
            cart_obj.save()
    #   if(cartIid.quantity == 0):
    #       cartIid.delete()
      return Response({'error':False, 'message':'quantity decrease'},status=200)

class DeleteCartItem(APIView):

    def post(self,request):
      cartIid = CartItem.objects.get(id=request.data['id'])
      cart_obj = cartIid.cart
      cart_obj.total-=cartIid.subtotal
      cart_obj.save()
      cartIid.delete()
      return Response({'error':False, 'message':'Cart item Deleted successfully'},status=200)
    
class Delatefullcart(APIView):
    def post(self, request):
        try:
            cart_obj = Cart.objects.get(id=request.data['id'])

            # Delete only CartItems (not the cart itself)
            cart_items = CartItem.objects.filter(cart=cart_obj)
            cart_items.delete()

            # Reset total
            cart_obj.total = 0
            cart_obj.save()

            return Response({"message": "Cart cleared"})
        except Cart.DoesNotExist:
            return Response({"message": "Cart not found"}, status=404)
        except Exception as e:
            return Response({"message": "Something went wrong", "error": str(e)}, status=500)
    

class OrderViewset(viewsets.ViewSet):
    
    def list(self, request):
        order_cart = Order.objects.filter(cart__user=request.user)
        serializer = OrderSerializers(order_cart, many=True)
        return Response(serializer.data)
    

    def create(self, request):
        cart_id = request.data['id']
        cart_obj = Cart.objects.get(id=cart_id)

        email = request.data['email']
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        address = request.data['address']
        phone = request.data['phone']

    
        created_order = Order.objects.create(
            cart=cart_obj,
            email=email,
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            address=address,
            delivery=100,
            total=cart_obj.total + 100
        )

     
        cart_items = CartItem.objects.filter(cart=cart_obj)
        for item in cart_items:
            OrderedItem.objects.create(
                order=created_order,
                item=item.item,
                price=item.price,
                quantity=item.quantity,
                subtotal=item.subtotal
            )

        return Response({'message': 'Order received'})



