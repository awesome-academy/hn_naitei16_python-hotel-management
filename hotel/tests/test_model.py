from hotel.views import room_profile
from django import utils
from django.test import TestCase
from hotel.models import Room, RoomService, RoomImage, Service, Booking, User, Bill
import datetime
from ..utils.constants import ROOM_TYPES, STATUS_TYPE

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_id = User.objects.create(
            email= 'test1@gmail.com',
            phoneNumber= '+84399695122',
            first_name= 'FName',
            last_name= 'LName',
            username= 'test_user1'
        ).pk

    def test_first_name_label(self):
        test_user = User.objects.get(id=self.user_id)
        field_label = test_user._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        test_user = User.objects.get(id=self.user_id)
        field_label = test_user._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_email_unique(self):
        user = User.objects.get(id=self.user_id)
        unique = user._meta.get_field('email').unique
        self.assertEqual(unique, True)
    
    def test_phone_number_unique(self):
        user = User.objects.get(id=self.user_id)
        unique = user._meta.get_field('phoneNumber').unique
        self.assertEqual(unique, True)    

class RoomModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.room = Room.objects.create(capacity = 4, numberOfBeds = 2, roomType= ROOM_TYPES[1], room_price = 50, description = 'Description for Room test 1' ).pk
        
    def test_room_type_max_length(self):
        room = Room.objects.get(id = self.room)
        max_length = room._meta.get_field('roomType').max_length
        self.assertEqual(max_length, 20)

    def test_description_max_length(self):
        room = Room.objects.get(id = self.room)
        max_length = room._meta.get_field('description').max_length
        self.assertEqual(max_length, 100)
        
class BookingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(email= 'test1@gmail.com', username= 'test_user1', phoneNumber= '+84399695122')
        room = Room.objects.create(capacity = 4, numberOfBeds = 2, roomType= ROOM_TYPES[1], room_price = 50, description = 'Description for Room test 1' )
        start_date = datetime.date.today() + datetime.timedelta(days= 2)
        end_date = datetime.date.today() + datetime.timedelta(days= 5)
        cls.booking_id = Booking.objects.create(user= test_user1, room_id= room, start_date= start_date, end_date= end_date, status= STATUS_TYPE[1][1], room_price= 450.0).pk
        
    def test_booking_status_max_length(self):
        booking = Booking.objects.get(booking_id = self.booking_id)
        max_length = booking._meta.get_field('status').max_length
        self.assertEqual(max_length, 20)
        
class ServiceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.service = Service.objects.create(service_name = 'Buffet', service_price= 50, description= 'Description for Service test 1').pk
        
    def test_service_name_max_length(self):
        service = Service.objects.get(id = self.service)
        max_length = service._meta.get_field('service_name').max_length
        self.assertEqual(max_length, 20)

class RoomServiceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(email= 'test1@gmail.com', username= 'test_user1', phoneNumber= '+84399695122')
        room = Room.objects.create(capacity = 4, numberOfBeds = 2, roomType= ROOM_TYPES[1], room_price = 50, description = 'Description for Room test 1' )
        start_date = datetime.date.today() + datetime.timedelta(days= 2)
        end_date = datetime.date.today() + datetime.timedelta(days= 5)
        booking_id = Booking.objects.create(user= test_user1, room_id= room, start_date= start_date, end_date= end_date, status= STATUS_TYPE[1][1], room_price= 450.0)
        service_id = Service.objects.create(service_name = 'Buffet', service_price= 50, description= 'Description for Service test 1')
        cls.room_service = RoomService.objects.create(booking_id = booking_id, service_id = service_id, service_price = service_id.service_price).pk

    def test_string_represent(self):
        room_service = RoomService.objects.get(id = self.room_service)
        self.assertEqual(str(room_service),str(room_service.service_price))
    
class RoomImageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        room = Room.objects.create(capacity = 4, numberOfBeds = 2, roomType= ROOM_TYPES[1], room_price = 50, description = 'Description for Room test 1' )
        cls.room_image = RoomImage.objects.create(room_id = room, img_url = 'image/iamge1').pk
        
    def test_room_image_url_max_length(self):
        room_image = RoomImage.objects.get(id = self.room_image)
        max_length = room_image._meta.get_field('img_url').max_length
        self.assertEqual(max_length, 50)

class BillModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(email= 'test1@gmail.com', username= 'test_user1', phoneNumber= '+84399695122')
        room = Room.objects.create(capacity = 4, numberOfBeds = 2, roomType= ROOM_TYPES[1], room_price = 50, description = 'Description for Room test 1' )
        start_date = datetime.date.today() + datetime.timedelta(days= 2)
        end_date = datetime.date.today() + datetime.timedelta(days= 5)
        booking_id = Booking.objects.create(user= test_user1, room_id= room, start_date= start_date, end_date= end_date, status= STATUS_TYPE[1][1], room_price= 450.0)
        cls.bill = Bill.objects.create(booking_id = booking_id, totalAmount = 500, summary = 'Summary for Bill test 1').pk
        
    def test_string_represent(self):
        bill = Bill.objects.get( bill_id = self.bill)
        expected_text = f'{bill.summary} {bill.totalAmount}'
        self.assertEqual(str(bill), expected_text)
