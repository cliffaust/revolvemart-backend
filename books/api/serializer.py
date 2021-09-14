from rest_framework import serializers
from books.models import Book, BookImage, BookReview, Order, ShippingAddress, Cart, ShippingNote


class BookReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    name = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()
    date_posted = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BookReview
        exclude = ["book"]

    def get_name(self, instance):
        return (
            f"{instance.user.first_name} {instance.user.last_name}"
            if instance.user.first_name and instance.user.last_name
            else instance.user.email
        )

    def get_profile_pic(self, instance):
        return instance.user.profile_pic.url


class BookImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookImage
        exclude = ["book"]


class BookSerializer(serializers.ModelSerializer):
    slug = serializers.StringRelatedField(read_only=True)
    book_images = BookImageSerializer(many=True, read_only=True)
    views = serializers.SerializerMethodField()
    discount_percentage = serializers.FloatField(read_only=True)
    date_posted = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Book
        exclude = ["user"]

    def get_views(self, instance):
        return instance.views.count()


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        exclude = ["user"]


class ShippingNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingNote
        fields = ["note"]
        


class CartSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    total_book_price = serializers.FloatField(read_only=True)
    total_book_discount_price = serializers.FloatField(read_only=True)
    saving_amount = serializers.FloatField(read_only=True)
    final_price = serializers.FloatField(read_only=True)

    class Meta:
        model = Cart
        exclude = ["user"]
        read_only_fields = ("ordered",)


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    book = BookSerializer(read_only=True)
    total_price = serializers.FloatField(read_only=True)
    shipping_address = ShippingAddressSerializer(read_only=True)
    shipping_note = ShippingNoteSerializer(read_only=True)
    created_at = serializers.StringRelatedField(read_only=True)
    updated_at = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"


    def update(self, instance, validated_data):
        shipping_address_data = validated_data.pop('shipping_address')

        shipping_note_data = validated_data.pop('shipping_note')

        shipping_address = instance.shipping_address

        shipping_note = instance.shipping_note

        instance.being_delivered = validated_data.get('being_delivered', instance.being_delivered)
        instance.received = validated_data.get('received', instance.received)
        instance.paid = validated_data.get('paid', instance.paid)

        instance.on_board = validated_data.get('on_board', instance.on_board)
        instance.estimated_shipping_cost = validated_data.get('estimated_shipping_cost', instance.estimated_shipping_cost)
        instance.final_shipping_cost = validated_data.get('paid', instance.final_shipping_cost)

        instance.quantity = validated_data.get('quantity', instance.quantity)

        instance.save()

        shipping_note.note = shipping_note_data.get('note', shipping_note.note)

        shipping_address.address = shipping_address_data.get('address', shipping_address.address)
        shipping_address.town = shipping_address_data.get('town', shipping_address.town)
        shipping_address.region = shipping_address_data.get('region', shipping_address.region)

        shipping_address.save()

        shipping_note.save()

        return instance

