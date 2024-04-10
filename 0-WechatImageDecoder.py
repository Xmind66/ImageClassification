
import sys
import re
import os

class WechatImageDecoder:
    def __init__(self, dat_file):
        dat_file = dat_file.lower()

        decoder = self._match_decoder(dat_file)
        decoder(dat_file)

    def _match_decoder(self, dat_file):
        decoders = {
            r'.+\.dat$': self._decode_pc_dat,
            r'cache\.data\.\d+$': self._decode_android_dat,
            None: self._decode_unknown_dat,
        }

        for k, v in decoders.items():
            if k is not None and re.match(k, dat_file):
                return v
        return decoders[None]

    def _decode_pc_dat(self, dat_file):
        
        def do_magic(header_code, buf):
            return header_code ^ list(buf)[0] if buf else 0x00
        
        def decode(magic, buf):
            return bytearray([b ^ magic for b in list(buf)])
            
        def guess_encoding(buf):
            headers = {
                'jpg': (0xff, 0xd8),
                'png': (0x89, 0x50),
                'gif': (0x47, 0x49),
            }
            for encoding in headers:
                header_code, check_code = headers[encoding] 
                magic = do_magic(header_code, buf)
                _, code = decode(magic, buf[:2])
                if check_code == code:
                    return (encoding, magic)
            print('Decode failed')
            sys.exit(1) 
        
        with open(dat_file, 'rb') as f:
            buf = bytearray(f.read())
        file_type, magic = guess_encoding(buf)

        # 修改保存图片的路径为当前子目录
        result_folder = os.path.join(os.getcwd(), 'Decoded Image')
        if not os.path.exists(result_folder):
            os.makedirs(result_folder)
        img_file = os.path.join(result_folder, os.path.basename(re.sub(r'.dat$', '.' + file_type, dat_file)))
        with open(img_file, 'wb') as f:
            new_buf = decode(magic, buf)
            f.write(new_buf)

    def _decode_android_dat(self, dat_file):
        with open(dat_file, 'rb') as f:
            buf = f.read()

        last_index = 0
        for i, m in enumerate(re.finditer(b'\xff\xd8\xff\xe0\x00\x10\x4a\x46', buf)):
            if m.start() == 0:
                continue

            # 修改保存图片的路径为当前子目录
            result_folder = os.path.join(os.getcwd(), 'Decoded Image')
            if not os.path.exists(result_folder):
                os.makedirs(result_folder)
            imgfile = os.path.join(result_folder, f'{os.path.basename(dat_file)}_{i}.jpg')
            with open(imgfile, 'wb') as f:
                f.write(buf[last_index: m.start()])
            last_index = m.start()

    def _decode_unknown_dat(self, dat_file):
        raise Exception('Unknown file type')



##################################################

image_folder = input("请输入微信加密图片文件夹：")
result_folder = os.path.join(os.getcwd(), 'result')
if not os.path.exists(result_folder):
    os.makedirs(result_folder)

for dirpath, dirnames, filenames in os.walk(image_folder):
    for filename in filenames:
        if len(filename) == 36 and filename.endswith('.dat'):
            image_path = os.path.join(dirpath, filename)
            print(image_path)
            WechatImageDecoder(image_path)
