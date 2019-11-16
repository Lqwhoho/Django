from django.http import JsonResponse
from sign.models import Event, Guest
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.utils import IntegrityError
import time


# 添加发布会接口
def add_event(request):
    eid = request.POST.get('eid', )     # 发布会id
    name = request.POST.get('name', )   # 发布会标题
    limit = request.POST.get('limit', )     # 限制人数
    status = request.POST.get('status', )   # 状态
    address = request.POST.get('address', )      # 地址
    start_time = request.POST.get('start_time', )   # 发布会时间

    if eid == ''or name == '' or limit == ''or address == ''or start_time == '':        # eid等字段均不能为空
        # 返回相对应的状态码和提示(将字典转化为JSON格式返回给客户端)
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    # 判断发布会id(eid)和名称(name)是否存在，如果存在说明数据重复，需返回相应的状态码和提示消息
    result = Event.objects.filter(id=eid)
    if result:
        return JsonResponse({'status': 10022, 'message': 'event is already exists'})

    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({'status': 10023, 'message': 'event name already exists'})

    # 发布会状态不是必传字段，如果为空，则将状态设置为1(True)
    if status == '':
        status = 1

    # 将数据插入Event表，如果日期格式错误，则抛出ValidationError异常，异常处理接收该异常并返回相应的状态码和提示
    try:
        Event.objects.create(id=eid, name=name, limit=limit, address=address, status=status, start_time=start_time)
    except ValidationError as e:
        error = 'start_time format error.It must be in YYYY-MM-DD HH:MM:SS format'
        return JsonResponse({'status': 10024, 'message': error})

    # 数据插入成功，返回状态码200和'add event success'的提示
    return JsonResponse({'status': 200, 'message': 'add event success'})


# 查询发布会接口
def get_event_list(request):
    eid = request.GET.get("eid", )
    name = request.GET.get("name", )

    if eid == ''and name == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    # 如果发布会id(eid)不为空，则优先使用发布会id查询，因为id具有唯一性，所以，查询的结果只会是一条
    # 将查询结果以字典的形式存放到event中，必将event作为借口返回字典中data对应的值
    if eid != '':
        event = {}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})
        else:
            event['name'] = result.name
            event['limit'] = result.limit
            event['status'] = result.status
            event['address'] = result.address
            event['start_time'] = result.start_time
            return JsonResponse({'status': 200, 'message': 'success', 'data': event})

    if name != '':
        datas = []
        results = Event.objects.filter(name__contains=name)
        if results:
            for r in results:
                event = dict()
                event['name'] = r.name
                event['limit'] = r.limit
                event['status'] = r.status
                event['address'] = r.address
                event['start_time'] = r.start_time
                datas.append(event)
                return JsonResponse({'status': 200, 'message': 'success', 'data': datas})
        else:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})


# 添加嘉宾接口
def add_guest(request):
    eid = request.POST.get('eid', )     # 关联发布会ID
    realname = request.POST.get('realname', )   # 姓名
    phone = request.POST.get('phone', )     # 手机号
    email = request.POST.get('email', )     # 邮箱

    if eid == '' or realname == '' or phone == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'status': 10022, 'message': 'event id null'})

    result = Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({'status': 10023, 'message': 'event status is not available'})

    event_limit = Event.objects.get(id=eid).limit   # 发布会限制人数
    guest_limit = Guest.objects.filter(event_id=eid)    # 发布会已添加的嘉宾数

    if len(guest_limit) >= event_limit:
        return JsonResponse({'status': 10024, 'message': 'event number is full'})

    event_time = Event.objects.get(id=eid).start_time   # 发布会时间
    etime = str(event_time).split(".")[0]
    timeArray = time.strptime(etime, "%Y-%m-%d %H:%M:%S")
    e_time = int(time.mktime(timeArray))

    now_time = str(time.time())     # 当前时间
    ntime = now_time.split(".")[0]
    n_time = int(ntime)

    if n_time >= e_time:
        return JsonResponse({'status': 10025, 'message': 'event has started'})

    try:
        Guest.objects.create(realname=realname, phone=int(phone), email=email, sign=0, event_id=int(eid))
    except IntegrityError:
        return JsonResponse({'status': 10026, 'message': 'the event guest phone number repeat'})

    return JsonResponse({'status': 200, 'message': 'add guest success'})


# 发布会查询
def get_event_list(request):

    eid = request.GET.get("eid", "")      # 发布会id
    name = request.GET.get("name", "")    # 发布会名称

    if eid == '' and name == '':
        return JsonResponse({'status':10021,'message':'parameter error'})

    if eid != '':
        event = {}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status':10022, 'message':'query result is empty'})
        else:
            event['eid'] = result.id
            event['name'] = result.name
            event['limit'] = result.limit
            event['status'] = result.status
            event['address'] = result.address
            event['start_time'] = result.start_time
            return JsonResponse({'status':200, 'message':'success', 'data':event})

    if name != '':
        datas = []
        results = Event.objects.filter(name__contains=name)
        if results:
            for r in results:
                event = dict()
                event['eid'] = r.id
                event['name'] = r.name
                event['limit'] = r.limit
                event['status'] = r.status
                event['address'] = r.address
                event['start_time'] = r.start_time
                datas.append(event)
            return JsonResponse({'status':200, 'message':'success', 'data':datas})
        else:
            return JsonResponse({'status':10022, 'message':'query result is empty'})


# 嘉宾查询接口
def get_guest_list(request):
    eid = request.GET.get("eid", "")       # 关联发布会id
    phone = request.GET.get("phone", "")   # 嘉宾手机号

    if eid == '':
        return JsonResponse({'status': 10021, 'message': 'eid cannot be empty'})

    if eid != '' and phone == '':
        datas = []
        results = Guest.objects.filter(event_id=eid)
        if results:
            for r in results:
                guest = dict()
                guest['realname'] = r.realname
                guest['phone'] = r.phone
                guest['email'] = r.email
                guest['sign'] = r.sign
                datas.append(guest)
            return JsonResponse({'status': 200, 'message': 'success', 'data': datas})
        else:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})

    if eid != '' and phone != '':
        guest = {}
        try:
            result = Guest.objects.get(phone=phone, event_id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})
        else:
            guest['realname'] = result.realname
            guest['phone'] = result.phone
            guest['email'] = result.email
            guest['sign'] = result.sign
            return JsonResponse({'status':200, 'message': 'success', 'data': guest})


# 用户签到接口
def user_sign(request):
    eid = request.POST.get('eid', '')       # 发布会id
    phone = request.POST.get('phone', '')   # 嘉宾手机号

    if eid == '' or phone == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'status': 10022, 'message': 'event id null'})

    result = Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({'status': 10023, 'message': 'event status is not available'})

    event_time = Event.objects.get(id=eid).start_time     # 发布会时间
    timeArray = time.strptime(str(event_time), "%Y-%m-%d %H:%M:%S")
    e_time = int(time.mktime(timeArray))

    now_time = str(time.time())          # 当前时间
    ntime = now_time.split(".")[0]
    n_time = int(ntime)

    if n_time >= e_time:
        return JsonResponse({'status': 10024, 'message': 'event has started'})

    result = Guest.objects.filter(phone=phone)
    if not result:
        return JsonResponse({'status': 10025, 'message':'user phone null'})

    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return JsonResponse({'status': 10026, 'message':'user did not participate in the conference'})

    result = Guest.objects.get(event_id=eid, phone=phone).sign
    if result:
        return JsonResponse({'status': 10027, 'message':'user has sign in'})
    else:
        Guest.objects.filter(phone=phone).update(sign='1')
        return JsonResponse({'status': 200, 'message': 'sign success'})
