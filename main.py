from datetime import timedelta, timezone
from pystyle import Write, Colors, System
import base64, json, datetime
from sys import exit

try: 
    from Cryptodome.Cipher import AES
    from Cryptodome.Util import Padding
        
except ImportError:
    from Crypto.Cipher import AES
    from Crypto.Util import Padding
    
def load_file(file_path, mode='rb'):
    with open(file_path, mode) as file_handle:
        return file_handle.read().decode('utf-8')

def _get_authentication_key_data(file_path, pin):
    try:
        file_content = load_file(file_path)
        iv = '\x00' * 16
        cipher = AES.new((pin + pin + pin + pin).encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8"))
        decoded = Padding.unpad(padded_data=cipher.decrypt(base64.b64decode(file_content)),
                                block_size=16)
        return json.loads(decoded.decode('utf-8'))
    except ValueError:
        return ValueError
    except Exception:
        return Exception

def save_data(data, pin, outname):
    try:
        raw = bytes(Padding.pad(data_to_pad=json.dumps(data).encode('utf-8'), block_size=16))
        iv = '\x00' * 16
        cipher = AES.new((str(pin) + str(pin) + str(pin) + str(pin)).encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
        encrypted_data = base64.b64encode(cipher.encrypt(raw)).decode('utf-8')
        file = open(f'{outname}.key', 'w')
        file.write(encrypted_data)
        file.close()
        
        Write.Print("Done !", Colors.red_to_black, 0.01)
    except Exception:
        Write.Print("An error occurred while creating the file", Colors.red_to_black, 0.01)

def expiration_changer(file_path, pin, days, outname):
    try:
        data = _get_authentication_key_data(file_path=file_path, pin=pin)
    
        if data == ValueError:
            Write.Print("Your pin is not correct !", Colors.red_to_black, 0.01)
        
        elif data == Exception:
            Write.Print(f"An error has occurred: {data}", Colors.red_to_black, 0.01)
        
        else:
            data['timestamp'] = int(((datetime.datetime.now(timezone.utc) + timedelta(days=days)) - datetime.datetime(year=1970, month=1, day=1, tzinfo=datetime.timezone.utc)).total_seconds())
            save_data(data, pin=pin, outname=outname)
    
    except Exception as e:
        print(f'An error has occurred: {e}')

def enter():
    path = Write.Input('Please enter the path of your key file: ', Colors.red_to_black, 0.01)
    path = path if path != '' else None
    if not path:
        System.Clear()
        Write.Print('Please enter the path !', Colors.red_to_black, 0.01)
        exit()

    pin = Write.Input('Please enter the pin of your key file: ', Colors.red_to_black, 0.01)
    pin = pin if pin != '' else None
    if not pin:
        System.Clear()
        Write.Print('Please enter the pin', Colors.red_to_black, 0.01)
        exit()
    
    days = Write.Input('Please enter the number of days before your key file expires (just enter = 5days): ', Colors.red_to_black, 0.01)
    days = days if days != '' else 5
    
    outname = Write.Input('Please enter the name of your out key file (just enter = NFAuthentication): ', Colors.red_to_black, 0.01)
    outname = outname if outname != '' else "NFAuthentication"
    
    expiration_changer(path, pin, int(days), outname)
    
enter()