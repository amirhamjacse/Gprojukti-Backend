EMPLOYEE_OFFICE_HOURS_LIST=[
    {
        'day': 'SATURDAY',
        'type': 'REGULAR',
        'start_time': '09:00',
        'end_time': '06:00',
        'grace_time': '09:20',
    },
    {
        'day': 'SUNDAY',
        'type': 'REGULAR',
        'start_time': '09:00',
        'end_time': '06:00',
        'grace_time': '09:20',
    },
    {
        'day': 'MONDAY',
        'type': 'REGULAR',
        'start_time': '09:00',
        'end_time': '06:00',
        'grace_time': '09:20',
    },
    {
        'day': 'TUESDAY',
        'type': 'REGULAR',
        'start_time': '09:00',
        'end_time': '06:00',
        'grace_time': '09:20',
    },
    {
        'day': 'WEDNESDAY',
        'type': 'REGULAR',
        'start_time': '09:00',
        'end_time': '06:00',
        'grace_time': '09:20',
    },
    {
        'day': 'THURSDAY',
        'type': 'REGULAR',
        'start_time': '09:00',
        'end_time': '06:00',
        'grace_time': '09:20',
    },
    {
        'day': 'SATURDAY',
        'type': 'REGULAR',
        'start_time': '05:00',
        'end_time': '12:00',
        'grace_time': '05:20',
    },
    {
        'day': 'SUNDAY',
        'type': 'REGULAR',
        'start_time': '05:00',
        'end_time': '12:00',
        'grace_time': '05:20',
    },
    {
        'day': 'MONDAY',
        'type': 'REGULAR',
        'start_time': '05:00',
        'end_time': '12:00',
        'grace_time': '05:20',
    },
    {
        'day': 'TUESDAY',
        'type': 'REGULAR',
        'start_time': '05:00',
        'end_time': '12:00',
        'grace_time': '05:20',
    },
    {
        'day': 'WEDNESDAY',
        'type': 'REGULAR',
        'start_time': '05:00',
        'end_time': '12:00',
        'grace_time': '05:20',
    },
    {
        'day': 'THURSDAY',
        'type': 'REGULAR',
        'start_time': '05:00',
        'end_time': '12:00',
        'grace_time': '05:20',
    },
    
]

SUBSCRIPTION_PLAN_LIST = [
    {
        'name':'Free',
        'slug':'free',
        'plan':'FREE',
        'plan_type':'MONTH',
        'plan_value':3,
        'category_limit':30,
        'product_limit':300,
        'employee_limit':30,
        'shop_limit':30,
        'is_active':True
    },
    {
        'name':'Basic',
        'slug':'basic',
        'plan':'BASIC',
        'plan_type':'YEARS',
        'plan_value':2,
        'category_limit':70,
        'product_limit':600,
        'employee_limit':90,
        'shop_limit':40,
        'is_active':True
    },
    {
        'name':'Lifetime',
        'slug':'life-time',
        'plan':'PREMIUM',
        'plan_type':'LIFETIME',
        'plan_value':3,
        'category_limit':30,
        'product_limit':300,
        'employee_limit':30,
        'shop_limit':30,
        'is_active':True
    }
]

COMPANY_TYPE_LIST = [
    {
        'name':'Marketplace',
        'slug':'market-place',
        'is_active':True
    },
    {
        'name':'Service Center',
        'slug':'service-center',
        'is_active':True
    }
]

SLIDER_LIST = [
    {
        'name':'Pre-owned Laptop',
        'slug':'pre-owned-laptop',
        'image':'https://gprmain.sgp1.cdn.digitaloceanspaces.com/dev-gprojukti/test/e660fed137684c4ba3cb71a5ff79560f-Pre-ownedlaptopbanner.jpg',
        'is_active':True,
        'is_slider':True,
        'is_popup':False,
        'serial_no':1
    },
    {
        'name':'Router Banner',
        'slug':'proton-feature-phone',
        'image':'https://gprmain.sgp1.cdn.digitaloceanspaces.com/dev-gprojukti/test/2fec7a60f2f543269d15deed294d7343-58f294401b95489091560441fa6e6ae1-Router-website-banner1.jpg',
        'is_active':True,
        'is_slider':True,
        'is_popup':False,
        'serial_no':2
    },
    {
        'name':'Proton Feature Phone',
        'slug':'proton-feature-phone-2',
        'image':'https://gprmain.sgp1.cdn.digitaloceanspaces.com/dev-gprojukti/test/7641a5787720464ca91cfc286833bb51-ProtonFeaturePhoneWebBanner(2).jpg',
        'is_active':True,
        'is_slider':True,
        'is_popup':False,
        'serial_no':3
    },
    {
        'name':'Smartwatch Collection',
        'slug':'smart-watch-phone',
        'image':'https://gprmain.sgp1.cdn.digitaloceanspaces.com/dev-gprojukti/test/7516977494e84d1cbe4e8a6254ee30f2-Smartwatch-collection-promo-banner.jpg',
        'is_active':True,
        'is_slider':False,
        'is_popup':False,
        'serial_no':1
    },
    # {
    #     'name':'Smart Watch Phone 2',
    #     'slug':'smart-watch-phone-2',
    #     'image':'https://gprmain.sgp1.cdn.digitaloceanspaces.com/gprojukti-v2-test/product/accec73243004d9799101441991a5933-83c48772-04a1-42ef-8dd2-12908ee0bbbf.png',
    #     'is_active':True,
    #     'is_slider':False,
    #     'is_popup':True,
    #     'serial_no':2
    # }
]

DELIVERY_METHOD_LIST = [
    {
        'delivery_type':'HOME_DELIVERY',
        'slug':'home_delivery',
        'delivery_charge':35.0
    },
    {
        'delivery_type':'STORE_SELL',
        'slug':'store-sell',
        'delivery_charge':0.0
    },
    {
        'delivery_type':'SHOP_PICKUP',
        'slug':'shop-pickup',
        'delivery_charge':0.0
    },
    {
        'delivery_type':'EXPRESS_HOME_DELIVERY_INSIDE_DHAKA',
        'slug':'express-home-delivery-inside-dhaka',
        'delivery_charge':120.0
    },
    {
        'delivery_type':'EXPRESS_HOME_DELIVERY_OUTSIDE_DHAKA',
        'slug':'express-home-delivery-outside-dhaka',
        'delivery_charge':200.0
    },
    {
        'delivery_type':'EXPRESS_DELIVERY_FROM_STORE_PICKUP_INSIDE_DHAKA',
        'slug':'express-delivery-from-store-pickup-inside-dhaka',
        'delivery_charge':120.0
    },
    {
        'delivery_type':'EXPRESS_DELIVERY_FROM_STORE_PICKUP_OUTSIDE_DHAKA',
        'slug':'express-delivery-from-store-pickup-outside-dhaka',
        'delivery_charge':200.0
    },
    {
        'delivery_type':'INSIDE_DHAKA',
        'slug':'inside-dhaka',
        'delivery_charge':120.0
    },
    {
        'delivery_type':'OUTSIDE_DHAKA',
        'slug':'outside-dhaka',
        'delivery_charge':200.0
    },
    {
        'delivery_type':'SAME_DAY_DELIVERY',
        'slug':'same-day-delivery',
        'delivery_charge': 120.0
    },
    {
        'delivery_type':'SHOP_TO_HOME_DELIVERY',
        'slug':'shop-to-home-delivery',
        'delivery_charge': 35.0
    },
]

[
    "https://gprmain.sgp1.cdn.digitaloceanspaces.com/gprojukti-v2-test/product/fa8c1830d8db4a7d9139f20feb8ff0c8-6badb75d-d9a7-40a5-9e63-77111968ecbf.png",
    "https://gprmain.sgp1.cdn.digitaloceanspaces.com/gprojukti-v2-test/product/e151ddf3378a43729a26f52282dddf09-13ff3bda-491e-4587-8d7f-37f35bdc2a39.png",
    "https://gprmain.sgp1.cdn.digitaloceanspaces.com/gprojukti-v2-test/product/24b0eff6f9b64129a0a4e0ce80750fc3-3a6999f2-42bf-4895-92a7-851dbfc5bf4b.png",
    "https://gprmain.sgp1.cdn.digitaloceanspaces.com/gprojukti-v2-test/product/3b830b5687e24a9d80b294c027fbe952-b7d727e9-764c-44a4-8e57-b074808a09ba.png",
    "https://gprmain.sgp1.cdn.digitaloceanspaces.com/gprojukti-v2-test/product/ec2cb6da0bab4310a93f1ed991f970c7-ec383dcc-215e-4e53-8e02-c4fe508f1870.png",
    "https://gprmain.sgp1.cdn.digitaloceanspaces.com/gprojukti-v2-test/product/7e077d682b324fd6b5f349af48127400-ea3abd55-6d10-427d-a6b1-ab568d7de22f.png",
    "https://gprmain.sgp1.cdn.digitaloceanspaces.com/gprojukti-v2-test/product/0b9e999103b1464fa3d0fed38a34dbbd-9d308624-fc3f-4950-b929-6361f08fb309.png",
    "https://gprmain.sgp1.cdn.digitaloceanspaces.com/gprojukti-v2-test/product/e2e21ebb24eb49ffabd5d3869b2d0a30-eff292aa-142f-498b-b216-b0410e81d5f5.png"
]

PAYMENT_TYPE_LIST = [
    {
        'name':'Bkash',
        'slug':'bkash',
        'logo':'https://gprmain.sgp1.cdn.digitaloceanspaces.com/gprojukti-v2-test/product/e2e21ebb24eb49ffabd5d3869b2d0a30-eff292aa-142f-498b-b216-b0410e81d5f5.png',
        'is_active':True
    },
    {
        'name': 'Nagad',
        'slug': 'nagad',
        'logo': 'https://gprmain.sgp1.cdn.digitaloceanspaces.com/gprojukti-v2-test/product/3b830b5687e24a9d80b294c027fbe952-b7d727e9-764c-44a4-8e57-b074808a09ba.png',
        'is_active': True
    },
    {
        'name': 'Rocket',
        'slug': 'rocket',
        'logo': 'https://gprmain.sgp1.cdn.digitaloceanspaces.com/gprojukti-v2-test/product/24b0eff6f9b64129a0a4e0ce80750fc3-3a6999f2-42bf-4895-92a7-851dbfc5bf4b.png',
        'is_active': True
    },
    {
        'name': 'SureCash',
        'slug': 'sure-cash',
        'logo': 'https://gprmain.sgp1.cdn.digitaloceanspaces.com/gprojukti-v2-test/product/e151ddf3378a43729a26f52282dddf09-13ff3bda-491e-4587-8d7f-37f35bdc2a39.png',
        'is_active': True
    },
    {
        'name': 'UCash',
        'slug': 'u-cash',
        'logo': 'https://businesspostbd.com/files/thumbs/daily-media/2023/08/01/800x457/IDLC.png',
        'is_active': True
    },
    {
        'name': 'mCash',
        'slug': 'm-cash',
        'logo': 'https://gprmain.sgp1.cdn.digitaloceanspaces.com/gprojukti-v2-test/product/ec2cb6da0bab4310a93f1ed991f970c7-ec383dcc-215e-4e53-8e02-c4fe508f1870.png',
        'is_active': True
    },
    {
        'name': 'VISA',
        'slug': 'visa',
        'logo': 'https://gprmain.sgp1.cdn.digitaloceanspaces.com/gprojukti-v2-test/product/fa8c1830d8db4a7d9139f20feb8ff0c8-6badb75d-d9a7-40a5-9e63-77111968ecbf.png',
        'is_active': True
    },
    {
        'name': 'Cash On Delivery',
        'slug': 'cod',
        'logo': 'https://gprmain.sgp1.cdn.digitaloceanspaces.com/gprojukti-v2-test/product/0b9e999103b1464fa3d0fed38a34dbbd-9d308624-fc3f-4950-b929-6361f08fb309.png',
        'is_active': True
    },
    {
        'name': 'Master Card',
        'slug': 'master-card',
        'logo': 'https://gprmain.sgp1.cdn.digitaloceanspaces.com/gprojukti-v2-test/product/7e077d682b324fd6b5f349af48127400-ea3abd55-6d10-427d-a6b1-ab568d7de22f.png',
        'is_active': True
    }
]

COMPANY_LIST = [
    {
        'name':'G-Projukti.com',
        'slug':'g-projukti-com',
        'logo':'https://gprmain.sgp1.cdn.digitaloceanspaces.com/dev-gprojukti/test/8292bf8228d947f29d6ef7a6b55de87e-CategoryImage.jpg',
        'primary_phone':'01QQQQQQQQQ',
        'secondary_phone':'01WWWWWWWWW',
        'email':'info@gprojukti.com',
        'website_url':'https://www.gprojukti.com/',
        'vat_registration_no':'098765434567890',
        'registration_number':'876543345678764',
        'address':'House No: 156, Road-12, Block E, level 9,Kemal Ataturk Avenue, Banani, Dhaka -1212, Bangladesh',
        'starting_date':'2020-01-01',
        'company_owner':'gpro_owner@gmail.com',
        'subscription':'Lifetime',
        'company_type':'Marketplace',
        'payment_type':True,
        'currency':'BDT',
        'status':'ACTIVE',
        'is_active':True
    }, 
    # {
    #     'name':'KBG',
    #     'slug':'kbg',
    #     'logo':'https://kbg.com.bd/wp-content/uploads/2022/01/Layer-1-1.png',
    #     'primary_phone':'01EEEEEEEEE',
    #     'secondary_phone':'01RRRRRRRRR',
    #     'email':'info@kbg.com',
    #     'website_url':'https://www.kbg.com/',
    #     'vat_registration_no':'098765434567890',
    #     'registration_number':'876543345678764',
    #     'address':'House No: 156, Road-12, Block E, level 9,Kemal Ataturk Avenue, Banani, Dhaka -1212, Bangladesh',
    #     'starting_date':'2020-01-01',
    #     'company_owner':'kbg_owner@gmail.com',
    #     'subscription':'Lifetime',
    #     'company_type':'Marketplace',
    #     'payment_type':True,
    #     'currency':'BDT',
    #     'status':'ACTIVE',
    #     'is_active':True
    # }
]

TAX_CATEGORY_LIST = [
    {
        'name' : '5% Tax',
        'slug' : '5-tax',
        'value_in_percentage' : 5,
        'type' : 'SELL_TAX',
        'company' : 'g-projukti-com',
    },
    {
        'name' : '10% Tax',
        'slug' : '10-tax',
        'value_in_percentage' : 10,
        'type' : 'SELL_TAX',
        'company' : 'g-projukti-com',
    },
    {
        'name' : '5% Vat',
        'slug' : '5-vat',
        'value_in_percentage' : 5,
        'type' : 'BUY_TAX',
        'company' : 'g-projukti-com',
    },
    {
        'name' : '10% Vat',
        'slug' : '10-vat',
        'value_in_percentage' : 10,
        'type' : 'BUY_TAX',
        'company' : 'g-projukti-com',
    },
    
]

COUNTRY_LIST = [
    {
        'name' : 'Bangladesh',
        'slug' : 'bangladesh',
        'bn_name' : 'Bangladesh',
    },
    {
        'name' : 'USA',
        'slug' : 'usa',
        'bn_name' : 'USA',
    },
    {
        'name' : 'Chine',
        'slug' : 'chine',
        'bn_name' : 'Chine',
    }
]

DIVISION_LIST = [
    {
        'name': 'Dhaka',
        'slug': 'dhaka',
        'bn_name': 'ঢাকা',
        'country' : 'Bangladesh',
    },
    {
        'name': 'Chittagong',
        'slug': 'chittagong',
        'bn_name': 'চট্টগ্রাম',
        'country' : 'Bangladesh',
    },
    {
        'name': 'Rajshahi',
        'slug': 'rajshahi',
        'bn_name': 'রাজশাহী',
        'country' : 'Bangladesh',
    },
    {
        'name': 'Khulna',
        'slug': 'khulna',
        'bn_name': 'খুলনা',
        'country' : 'Bangladesh',
    },
    {
        'name': 'Barisal',
        'slug': 'barisal',
        'bn_name': 'বরিশাল',
        'country' : 'Bangladesh',
    },
    {
        'name': 'Sylhet',
        'slug': 'sylhet',
        'bn_name': 'সিলেট',
        'country' : 'Bangladesh',
    },
    {
        'name': 'Rangpur',
        'slug': 'rangpur',
        'bn_name': 'রংপুর',
        'country' : 'Bangladesh',
    },
    {
        'name': 'Mymensingh',
        'slug': 'mymensingh',
        'bn_name': 'ময়মনসিংহ',
        'country' : 'Bangladesh',
    }
]

DISTRICT_LIST = [
    {
        'name': 'Dhaka',
        'slug': 'dhaka',
        'bn_name': 'ঢাকা',
        'division': 'Dhaka'
    },
    {
        'name': 'Faridpur',
        'slug': 'faridpur',
        'bn_name': 'ফরিদপুর',
        'division': 'Dhaka'
    },
    {
        'name': 'Gazipur',
        'slug': 'gazipur',
        'bn_name': 'গাজীপুর',
        'division': 'Dhaka'
    },
    {
        'name': 'Gopalganj',
        'slug': 'gopalganj',
        'bn_name': 'গোপালগঞ্জ',
        'division': 'Dhaka'
    },
    {
        'name': 'Kishoreganj',
        'slug': 'kishoreganj',
        'bn_name': 'কিশোরগঞ্জ',
        'division': 'Dhaka'
    },
    {
        'name': 'Madaripur',
        'slug': 'madaripur',
        'bn_name': 'মাদারীপুর',
        'division': 'Dhaka'
    },
    {
        'name': 'Manikganj',
        'slug': 'manikganj',
        'bn_name': 'মানিকগঞ্জ',
        'division': 'Dhaka'
    },
    {
        'name': 'Munshiganj',
        'slug': 'munshiganj',
        'bn_name': 'মুন্সিগঞ্জ',
        'division': 'Dhaka'
    },
    {
        'name': 'Narayanganj',
        'slug': 'narayanganj',
        'bn_name': 'নারায়ণগঞ্জ',
        'division': 'Dhaka'
    },
    {
        'name': 'Narsingdi',
        'slug': 'narsingdi',
        'bn_name': 'নরসিংদী',
        'division': 'Dhaka'
    },
    {
        'name': 'Rajbari',
        'slug': 'rajbari',
        'bn_name': 'রাজবাড়ী',
        'division': 'Dhaka'
    },
    {
        'name': 'Shariatpur',
        'slug': 'shariatpur',
        'bn_name': 'শরীয়তপুর',
        'division': 'Dhaka'
    },
    {
        'name': 'Tangail',
        'slug': 'tangail',
        'bn_name': 'টাঙ্গাইল',
        'division': 'Dhaka'
    },
    {
        'name': 'Bandarban',
        'slug': 'bandarban',
        'bn_name': 'বান্দরবান',
        'division': 'Chittagong'
    },
    {
        'name': 'Brahmanbaria',
        'slug': 'brahmanbaria',
        'bn_name': 'ব্রাহ্মণবাড়িয়া',
        'division': 'Chittagong'
    },
    {
        'name': 'Chandpur',
        'slug': 'chandpur',
        'bn_name': 'চাঁদপুর',
        'division': 'Chittagong'
    },
    {
        'name': 'Chittagong',
        'slug': 'chittagong',
        'bn_name': 'চট্টগ্রাম',
        'division': 'Chittagong'
    },
    {
        'name': 'Comilla',
        'slug': 'comilla',
        'bn_name': 'কুমিল্লা',
        'division': 'Chittagong'
    },
    {
        'name': 'Coxs Bazar',
        'slug': 'coxs-bazar',
        'bn_name': 'কক্সবাজার',
        'division': 'Chittagong'
    },
    {
        'name': 'Feni',
        'slug': 'feni',
        'bn_name': 'ফেনী',
        'division': 'Chittagong'
    },
    {
        'name': 'Khagrachhari',
        'slug': 'khagrachhari',
        'bn_name': 'খাগড়াছড়ি',
        'division': 'Chittagong'
    },
    {
        'name': 'Lakshmipur',
        'slug': 'lakshmipur',
        'bn_name': 'লক্ষ্মীপুর',
        'division': 'Chittagong'
    },
    {
        'name': 'Noakhali',
        'slug': 'noakhali',
        'bn_name': 'নোয়াখালী',
        'division': 'Chittagong'
    },
    {
        'name': 'Rangamati',
        'slug': 'rangamati',
        'bn_name': 'রাঙ্গামাটি',
        'division': 'Chittagong'
    },
    {
        'name': 'Bogra',
        'slug': 'bogra',
        'bn_name': 'বগুড়া',
        'division': 'Rajshahi'
    },
    {
        'name': 'Joypurhat',
        'slug': 'joypurhat',
        'bn_name': 'জয়পুরহাট',
        'division': 'Rajshahi'
    },
    {
        'name': 'Naogaon',
        'slug': 'naogaon',
        'bn_name': 'নওগাঁ',
        'division': 'Rajshahi'
    },
    {
        'name': 'Natore',
        'slug': 'natore',
        'bn_name': 'নাটোর',
        'division': 'Rajshahi'
    },
    {
        'name': 'Chapainawabganj',
        'slug': 'chapainawabganj',
        'bn_name': 'চাঁপাইনবাবগঞ্জ',
        'division': 'Rajshahi'
    },
    {
        'name': 'Pabna',
        'slug': 'pabna',
        'bn_name': 'পাবনা',
        'division': 'Rajshahi'
    },
    {
        'name': 'Rajshahi',
        'slug': 'rajshahi',
        'bn_name': 'রাজশাহী',
        'division': 'Rajshahi'
    },
    {
        'name': 'Sirajganj',
        'slug': 'sirajganj',
        'bn_name': 'সিরাজগঞ্জ',
        'division': 'Rajshahi'
    },
    {
        'name': 'Bagerhat',
        'slug': 'bagerhat',
        'bn_name': 'বাগেরহাট',
        'division': 'Khulna'
    },
    {
        'name': 'Chuadanga',
        'slug': 'chuadanga',
        'bn_name': 'চুয়াডাঙ্গা',
        'division': 'Khulna'
    },
    {
        'name': 'Jessore',
        'slug': 'jessore',
        'bn_name': 'যশোর',
        'division': 'Khulna'
    },
    {
        'name': 'Jhenaidah',
        'slug': 'jhenaidah',
        'bn_name': 'ঝিনাইদহ',
        'division': 'Khulna'
    },
    {
        'name': 'Khulna',
        'slug': 'khulna',
        'bn_name': 'খুলনা',
        'division': 'Khulna'
    },
    {
        'name': 'Kushtia',
        'slug': 'kushtia',
        'bn_name': 'কুষ্টিয়া',
        'division': 'Khulna'
    },
    {
        'name': 'Magura',
        'slug': 'magura',
        'bn_name': 'মাগুরা',
        'division': 'Khulna'
    },
    {
        'name': 'Meherpur',
        'slug': 'meherpur',
        'bn_name': 'মেহেরপুর',
        'division': 'Khulna'
    },
    {
        'name': 'Narail',
        'slug': 'narail',
        'bn_name': 'নড়াইল',
        'division': 'Khulna'
    },
    {
        'name': 'Satkhira',
        'slug': 'satkhira',
        'bn_name': 'সাতক্ষীরা',
        'division': 'Khulna'
    },
    {
        'name': 'Barisal',
        'slug': 'barisal',
        'bn_name': 'বরিশাল',
        'division': 'Barisal'
    },
    {
        'name': 'Barguna',
        'slug': 'barguna',
        'bn_name': 'বরগুনা',
        'division': 'Barisal'
    },
    {
        'name': 'Bhola',
        'slug': 'bhola',
        'bn_name': 'ভোলা',
        'division': 'Barisal'
    },
    {
        'name': 'Jhalokati',
        'slug': 'jhalokati',
        'bn_name': 'ঝালকাঠি',
        'division': 'Barisal'
    },
    {
        'name': 'Patuakhali',
        'slug': 'patuakhali',
        'bn_name': 'পটুয়াখালী',
        'division': 'Barisal'
    },
    {
        'name': 'Pirojpur',
        'slug': 'pirojpur',
        'bn_name': 'পিরোজপুর',
        'division': 'Barisal'
    },
    {
        'name': 'Habiganj',
        'slug': 'habiganj',
        'bn_name': 'হবিগঞ্জ',
        'division': 'Sylhet'
    },
    {
        'name': 'Moulvibazar',
        'slug': 'moulvibazar',
        'bn_name': 'মৌলভীবাজার',
        'division': 'Sylhet'
    },
    {
        'name': 'Sunamganj',
        'slug': 'sunamganj',
        'bn_name': 'সুনামগঞ্জ',
        'division': 'Sylhet'
    },
    {
        'name': 'Sylhet',
        'slug': 'sylhet',
        'bn_name': 'সিলেট',
        'division': 'Sylhet'
    },
    {
        'name': 'Rangpur',
        'slug': 'rangpur',
        'bn_name': 'রংপুর',
        'division': 'Rangpur'
    },
    {
        'name': 'Dinajpur',
        'slug': 'dinajpur',
        'bn_name': 'দিনাজপুর',
        'division': 'Rangpur'
    },
    {
        'name': 'Gaibandha',
        'slug': 'gaibandha',
        'bn_name': 'গাইবান্ধা',
        'division': 'Rangpur'
    },
    {
        'name': 'Kurigram',
        'slug': 'kurigram',
        'bn_name': 'কুড়িগ্রাম',
        'division': 'Rangpur'
    },
    {
        'name': 'Lalmonirhat',
        'slug': 'lalmonirhat',
        'bn_name': 'লালমনিরহাট',
        'division': 'Rangpur'
    },
    {
        'name': 'Nilphamari',
        'slug': 'nilphamari',
        'bn_name': 'নীলফামারী',
        'division': 'Rangpur'
    },
    {
        'name': 'Panchagarh',
        'slug': 'panchagarh',
        'bn_name': 'পঞ্চগড়',
        'division': 'Rangpur'
    },
    {
        'name': 'Thakurgaon',
        'slug': 'thakurgaon',
        'bn_name': 'ঠাকুরগাঁও',
        'division': 'Rangpur'
    },
    {
        'name': 'Mymensingh',
        'slug': 'mymensingh',
        'bn_name': 'ময়মনসিংহ',
        'division': 'Mymensingh'
    },
    {
        'name': 'Jamalpur',
        'slug': 'jamalpur',
        'bn_name': 'জামালপুর',
        'division': 'Mymensingh'
    },
    {
        'name': 'Netrokona',
        'slug': 'netrokona',
        'bn_name': 'নেত্রকোণা',
        'division': 'Mymensingh'
    },
    {
        'name': 'Sherpur',
        'slug': 'sherpur',
        'bn_name': 'শেরপুর',
        'division': 'Mymensingh'
    }   
]

AREA_LIST = [
    {
        'name': 'Uttara',
        'slug': 'uttara',
        'bn_name': 'উত্তরা',
        'district': 'Dhaka'
    },
    {
        'name': 'Dhanmondi',
        'slug': 'dhanmondi',
        'bn_name': 'ধানমন্ডি',
        'district': 'Dhaka'
    },
    {
        'name': 'Gulshan',
        'slug': 'gulshan',
        'bn_name': 'গুলশান',
        'district': 'Dhaka'
    },
    {
        'name': 'Mirpur',
        'slug': 'mirpur',
        'bn_name': 'মিরপুর',
        'district': 'Dhaka'
    },
    {
        'name': 'Banani',
        'slug': 'banani',
        'bn_name': 'বানানী',
        'district': 'Dhaka'
    },
    {
        'name': 'Faridpur Sadar',
        'slug': 'faridpur-sadar',
        'bn_name': 'ফরিদপুর সদর',
        'district': 'Faridpur'
    },
    {
        'name': 'Boalmari',
        'slug': 'boalmari',
        'bn_name': 'বোয়ালমারী',
        'district': 'Faridpur'
    },
    {
        'name': 'Alfadanga',
        'slug': 'alfadanga',
        'bn_name': 'আলফাডাঙ্গা',
        'district': 'Faridpur'
    }, {
        'name': 'Gazipur Sadar',
        'slug': 'gazipur-sadar',
        'bn_name': 'গাজীপুর সদর',
        'district': 'Gazipur'
    },
    {
        'name': 'Tongi',
        'slug': 'tongi',
        'bn_name': 'টঙ্গী',
        'district': 'Gazipur'
    },
    {
        'name': 'Kaliakair',
        'slug': 'kaliakair',
        'bn_name': 'কালিয়াকৈর',
        'district': 'Gazipur'
    },
    {
        'name': 'Gopalganj Sadar',
        'slug': 'gopalganj-sadar',
        'bn_name': 'গোপালগঞ্জ সদর',
        'district': 'Gopalganj'
    },
    {
        'name': 'Tungipara',
        'slug': 'tungipara',
        'bn_name': 'টুংগীপাড়া',
        'district': 'Gopalganj'
    },
    {
        'name': 'Kashiani',
        'slug': 'kashiani',
        'bn_name': 'কাশিয়ানী',
        'district': 'Gopalganj'
    },
    {
        'name': 'Kishoreganj Sadar',
        'slug': 'kishoreganj-sadar',
        'bn_name': 'কিশোরগঞ্জ সদর',
        'district': 'Kishoreganj'
    },
    {
        'name': 'Bhairab',
        'slug': 'bhairab',
        'bn_name': 'ভৈরব',
        'district': 'Kishoreganj'
    },
    {
        'name': 'Kuliarchar',
        'slug': 'kuliarchar',
        'bn_name': 'কুলিয়ারচর',
        'district': 'Kishoreganj'
    },
    {
        'name': 'Madaripur Sadar',
        'slug': 'madaripur-sadar',
        'bn_name': 'মাদারীপুর সদর',
        'district': 'Madaripur'
    },
    {
        'name': 'Shibchar',
        'slug': 'shibchar',
        'bn_name': 'শিবচর',
        'district': 'Madaripur'
    },
    {
        'name': 'Kalkini',
        'slug': 'kalkini',
        'bn_name': 'কালকিনি',
        'district': 'Madaripur'
    },
    {
        'name': 'Chittagong Sadar',
        'slug': 'chittagong-sadar',
        'bn_name': 'চট্টগ্রাম সদর',
        'district': 'Chittagong'
    },
    {
        'name': 'Banshkhali',
        'slug': 'banshkhali',
        'bn_name': 'বাঁশখালী',
        'district': 'Chittagong'
    },
    {
        'name': 'Anwara',
        'slug': 'anwara',
        'bn_name': 'আনোয়ারা',
        'district': 'Chittagong'
    },
    {
        'name': 'Coxs Bazar Sadar',
        'slug': 'coxs-bazar-sadar',
        'bn_name': 'কক্সবাজার সদর',
        'district': 'Coxs Bazar'
    },
    {
        'name': 'Teknaf',
        'slug': 'teknaf',
        'bn_name': 'টেকনাফ',
        'district': 'Coxs Bazar'
    },
    {
        'name': 'Ukhia',
        'slug': 'ukhia',
        'bn_name': 'উখিয়া',
        'district': 'Coxs Bazar'
    },
    {
        'name': 'Noakhali Sadar',
        'slug': 'noakhali-sadar',
        'bn_name': 'নোয়াখালী সদর',
        'district': 'Noakhali'
    },
    {
        'name': 'Senaorhat',
        'slug': 'senaorhat',
        'bn_name': 'সেনারহাট',
        'district': 'Noakhali'
    },
    {
        'name': 'Begumganj',
        'slug': 'begumganj',
        'bn_name': 'বেগমগঞ্জ',
        'district': 'Noakhali'
    },
    {
        'name': 'Rajshahi Sadar',
        'slug': 'rajshahi-sadar',
        'bn_name': 'রাজশাহী সদর',
        'district': 'Rajshahi'
    },
    {
        'name': 'Puthia',
        'slug': 'puthia',
        'bn_name': 'পুঠিয়া',
        'district': 'Rajshahi'
    },
    {
        'name': 'Bagha',
        'slug': 'bagha',
        'bn_name': 'বাঘা',
        'district': 'Rajshahi'
    },
    {
        'name': 'Khulna Sadar',
        'slug': 'khulna-sadar',
        'bn_name': 'খুলনা সদর',
        'district': 'Khulna'
    },
    {
        'name': 'Mongla',
        'slug': 'mongla',
        'bn_name': 'মংলা',
        'district': 'Khulna'
    },
    {
        'name': 'Dighalia',
        'slug': 'dighalia',
        'bn_name': 'দিঘলিয়া',
        'district': 'Khulna'
    },
    {
        'name': 'Sylhet Sadar',
        'slug': 'sylhet-sadar',
        'bn_name': 'সিলেট সদর',
        'district': 'Sylhet'
    },
    {
        'name': 'Beanibazar',
        'slug': 'beanibazar',
        'bn_name': 'বিয়ানিবাজার',
        'district': 'Sylhet'
    },
    {
        'name': 'Golapganj',
        'slug': 'golapganj',
        'bn_name': 'গোলাপগঞ্জ',
        'district': 'Sylhet'
    },
    {
        'name': 'Rangpur Sadar',
        'slug': 'rangpur-sadar',
        'bn_name': 'রংপুর সদর',
        'district': 'Rangpur'
    },
    {
        'name': 'Pirganj',
        'slug': 'pirganj',
        'bn_name': 'পীরগঞ্জ',
        'district': 'Rangpur'
    },
    {
        'name': 'Mithapukur',
        'slug': 'mithapukur',
        'bn_name': 'মিঠাপুকুর',
        'district': 'Rangpur'
    }
]



POS_AREA_LIST = [
    {
        'name': 'Dhaka Area 6',
        'slug': 'dhaka-area-6',
        'bn_name': 'Dhaka Area',
        'district': 'Dhaka',
        'phone': '01707415668'
    },
    {
        'name': 'Chittagong Area 10',
        'slug': 'chittagong-area-10',
        'bn_name': 'Chittagong Area 10',
        'district': 'Chittagong',
        'phone': '011791296364'
    },
    {
        'name': 'Rajshahi Area 2',
        'slug': 'rajshahi-area-2',
        'bn_name': 'Rajshahi Area 2',
        'district': 'Rajshahi',
        'phone': '01'
    },
    {
        'name': 'Khulna Area 13',
        'slug': 'khulna-area-13',
        'bn_name': 'Khulna Area 13',
        'district': 'Khulna',
        'phone': '01'
    },
    {
        'name': 'Barishal Area 12',
        'slug': 'barishal-area-12',
        'bn_name': 'Barishal Area 12',
        'district': 'Barishal',
        'phone': '01'
    },
    {
        'name': 'Sylhet Area 4',
        'slug': 'sylhet-area-4',
        'bn_name': 'Sylhet Area 4',
        'district': 'Sylhet',
        'phone': '01'
    },
    {
        'name': 'Rangpur Area 1',
        'slug': 'rangpur-area 1',
        'bn_name': 'Rangpur Area 1',
        'district': 'Rangpur',
        'phone': '01782864940'
    },
    {
        'name': 'Mymensingh Area 3',
        'slug': 'ymensingh-area-3',
        'bn_name': 'Mymensingh Area 3',
        'area': 'Mymensingh',
        'phone': '01'
    },
    {
        'name': 'Gazipur Area 5',
        'slug': 'gazipur-area-5',
        'bn_name': 'Gazipur Area 5',
        'district': 'Gazipur',
        'phone': '01'
    },
    {
        'name': 'Faridpur Area 7',
        'slug': 'faridpur-area-7',
        'bn_name': 'Faridpur Area 7',
        'district': 'Faridpur',
        'phone': '01'
    },
    {
        'name': 'Cumilla Area 8',
        'slug': 'cumilla-area-8',
        'bn_name': 'Cumilla Area 8',
        'district': 'Cumilla',
        'phone': '01'
    },
    {
        'name': 'Noakhali Area 9',
        'slug': 'noakhali-area-9',
        'bn_name': 'Noakhali Area 9',
        'area': 'Noakhali',
        'phone': '01770477881'
    },
    {
        'name': "Cox's Bazar Area 11",
        'slug': 'cox-bazar-area-11',
        'bn_name': "Cox's Bazar Area 11",
        'area': "Cox's Bazar",
        'phone': '011791296364'
    },
    
]

POS_REGION_LIST = [
    {
        'name': 'Region 1',
        'slug': 'region-1',
        'bn_name': 'Region 1',
        'pos_area': [
            {
                'name': 'Rangpur Area 1'
            },
            {
                'name': 'Rajshahi Area 2'
            }
        ]
    },
    {
        'name': 'Region 2',
        'slug': 'region-2',
        'bn_name': 'Region 2',
        'pos_area': [
            {
                'name': 'Mymensingh Area 3'
            },
            {
                'name': 'Sylhet Area 4'
            }
        ]
    },
    {
        'name': 'Region 3',
        'slug': 'region-3',
        'bn_name': 'Region 3',
        'pos_area': [
            {
                'name': 'Gazipur Area 5'
            },
            {
                'name': 'Dhaka Area 6'
            },
            {
                'name': 'Faridpur Area 7'
            }
        ]
    },
    {
        'name': 'Region 4',
        'slug': 'region-4',
        'bn_name': 'Region 4',
        'pos_area': [
            {
                'name': 'Cumilla Area 8'
            },
            {
                'name': 'Noakhali Area 9'
            }
        ]
    },
    {
        'name': 'Region 5',
        'slug': 'region-5',
        'bn_name': 'Region 5',
        'pos_area': [
            {
                'name': 'Chittagong Area 10'
            },
            {
                'name': "Cox's Bazar Area 11"
            }
        ]
    },
    {
        'name': 'Region 6',
        'slug': 'region-6',
        'bn_name': 'Region 6',
        'pos_area': [
            {
                'name': 'Barishal Area 12'
            },
            {
                'name': 'Khulna Area 13'
            }
        ]
    },
 
]


OFFICE_LOCATION_LIST = [
    {
        'name': 'GProjukti.com Head Office',
        'slug': 'g-projukti.com-head-office',
        'store_no': 'HO001',
        'bn_name': 'GProjukti.com - Head Office',
        'address': 'House No - 234, First-Floor, Head Office',
        'primary_phone': '0934567876',
        'map_link': 'https://gprojukti.com/',
        'area': 'Dhaka',
        'company': 'g-projukti-com',
        'office_type': 'HEAD_OFFICE',
        'pos_area': 'Dhaka Area',
        'is_shown_in_website': False
    },
    {
        'name': 'GProjukti.com Warehouse',
        'slug': 'g-projukti.com-warehouse',
        'store_no': 'WH001',
        'bn_name': 'GProjukti.com - Warehouse',
        'address': 'House No - 234, First-Floor, Warehouse',
        'primary_phone': '0934567876',
        'map_link': 'https://gprojukti.com/',
        'area': 'Dhaka',
        'company': 'g-projukti-com',
        'office_type': 'WAREHOUSE',
        'pos_area': 'Dhaka Area',
        'is_shown_in_website': False
    },
    {
        'name': 'GProjukti.com - Agargaon',
        'slug': 'g-projukti.com-agargaon',
        'store_no': 'SD001',
        'bn_name': 'GProjukti.com - Agargaon',
        'address': 'House No - 234, First-Floor, Agargaon',
        'primary_phone': '0934567876',
        'map_link': 'https://gprojukti.com/',
        'area': 'Dhaka',
        'company': 'g-projukti-com',
        'office_type': 'STORE',
        'pos_area': 'Dhaka Area'
    },
    {
        'name': 'GProjukti.com - Notun Bazar',
        'slug': 'g-projukti.com-notun-mirpur',
        'store_no': 'SD002',
        'bn_name': 'GProjukti.com - Notun Bazar',
        'address': 'House No - 234, First-Floor, Notun Bazar',
        'primary_phone': '0934567876',
        'map_link': 'https://gprojukti.com/',
        'area': 'Dhaka',
        'company': 'g-projukti-com',
        'office_type': 'STORE',
        'pos_area': 'Dhaka Area'
    },
    {
        'name': 'GProjukti.com - Agrabad',
        'slug': 'g-projukti.com-agrabad',
        'store_no': 'SD003',
        'bn_name': 'GProjukti.com - Agrabad',
        'address': 'House No - 234, First-Floor, Agrabad',
        'primary_phone': '0934567876',
        'map_link': 'https://gprojukti.com/',
        'area': 'Dhaka',
        'company': 'g-projukti-com',
        'office_type': 'STORE',
        'pos_area': 'Chittagong Area'
    },
    {
        'name': 'GProjukti.com - Coxs Bazar',
        'slug': 'g-projukti.com-coxs-bazar',
        'store_no': 'SD004',
        'bn_name': 'GProjukti.com - Coxs Bazar',
        'address': 'House No - 234, First-Floor, Coxs Bazar',
        'primary_phone': '0934567876',
        'map_link': 'https://gprojukti.com/',
        'area': 'Dhaka',
        'company': 'g-projukti-com',
        'office_type': 'STORE',
        'pos_area': 'Chittagong Area'
    },
    {
        'name': 'GProjukti.com - Cumilla',
        'slug': 'g-projukti.com-cumilla',
        'store_no': 'SD005',
        'bn_name': 'GProjukti.com - Cumilla',
        'address': 'House No - 234, First-Floor, Cumilla',
        'primary_phone': '0934567876',
        'map_link': 'https://gprojukti.com/',
        'area': 'Dhaka',
        'company': 'g-projukti-com',
        'office_type': 'STORE',
        'pos_area': 'Chittagong Area'
    },
    {
        'name': 'GProjukti.com - Malibug',
        'slug': 'g-projukti.com-malibug',
        'store_no': 'SD005',
        'bn_name': 'GProjukti.com - Malibug',
        'address': 'House No - 234, First-Floor, Malibug',
        'primary_phone': '0934567876',
        'map_link': 'https://gprojukti.com/',
        'area': 'Dhaka',
        'company': 'g-projukti-com',
        'office_type': 'STORE',
        'pos_area': 'Chittagong Area'
    }
]


SHOP_USER_LIST = [
    {
        "first_name": "GProjukti",
        "last_name": "Alongkar",
        "email": "alongkar@gprojukti.com",
        "phone": "alongkar@gprojukti.com",
        "password": "L8$u9IxY",
    }
]