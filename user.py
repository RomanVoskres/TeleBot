class User:
    phone_number = None
    first_name = None
    last_name = None
    user_id = None

    last_call_data = None

    procedure = None # Процедура которую хочет клиент

    appointment_zone = None  # запоминает зону макияжа пользователя
    comuflage = None # камуфляж true false
    communication_method = False  # запоминает метод связи с пользователем
    want_consult = False # Может хотеть на консультацию
    delalaTattoo_v_Broowushka = False
    delalaTattoo_v_zone = False
    want_send_photo = False

    training_appointment_id = None

    def __init__(self, phone_number, first_name, last_name, user_id, last_call_data, procedure, appointment_zone, comuflage, communication_method, want_consult, delalaTattoo_v_Broowushka,
                 delalaTattoo_v_zone, want_send_photo, training_appointment_id):
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = user_id

        self.last_call_data = last_call_data

        self.procedure = procedure

        self.appointment_zone = appointment_zone
        self.comuflage = comuflage
        self.communication_method = communication_method
        self.want_consult = want_consult
        self.delalaTattoo_v_Broowushka = delalaTattoo_v_Broowushka
        self.delalaTattoo_v_zone = delalaTattoo_v_zone
        self.want_send_photo = want_send_photo

        self.training_appointment_id = training_appointment_id
