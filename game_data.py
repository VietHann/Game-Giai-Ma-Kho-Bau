from crypto_algorithms import CryptoEngine

class GameData:
    
    def __init__(self):
        self.crypto_engine = CryptoEngine()
        self._generate_game_content()
    
    def _generate_game_content(self):
        
        self.rsa_keys = self.crypto_engine.generate_rsa_keys()
        
        self.levels = {
            1: {
                'title': 'Cấp độ 1: Mật mã Caesar',
                'story': 'Bạn tìm thấy một tờ giấy cũ trong rương gỗ. Trên đó có dòng chữ bí ẩn được viết bằng mật mã Caesar. Hãy giải mã để tìm manh mối đầu tiên!',
                'algorithm': 'caesar',
                'algorithm_name': 'Caesar Cipher',
                'instruction': 'Nhập số bước dịch chuyển (0-25):',
                'message': 'KHO BAU NAM O PHIA BEI',
                'shift': 3,
                'expected_result': 'KHO BAU NAM O PHIA BEI',
                'hint': 'Thử với số dịch chuyển từ 1 đến 10. Julius Caesar thường dùng số 3.',
                'points': 100
            },
            2: {
                'title': 'Cấp độ 2: Mật mã Vigenère', 
                'story': 'Sau khi giải mã thành công, bạn tìm thấy một bức thư khác phức tạp hơn. Lần này sử dụng mật mã Vigenère với từ khóa bí mật!',
                'algorithm': 'vigenere',
                'algorithm_name': 'Vigenère Cipher',
                'instruction': 'Nhập từ khóa (chỉ chữ cái):',
                'message': 'CAY SO CO NAM DUOI GAM',
                'keyword': 'TREASURE',
                'expected_result': 'CAY SO CO NAM DUOI GAM',
                'hint': 'Từ khóa liên quan đến kho báu. Thử "TREASURE" hoặc "GOLD".',
                'points': 150
            },
            3: {
                'title': 'Cấp độ 3: Mật mã RSA',
                'story': 'Bạn đến gần hơn với kho báu! Bây giờ bạn phải đối mặt với mật mã RSA - một trong những thuật toán mạnh nhất!',
                'algorithm': 'rsa',
                'algorithm_name': 'RSA Encryption',
                'instruction': 'Nhập khóa riêng tư dưới dạng (n, d):',
                'message': '',  # Will be generated
                'private_key': None,  # Will be set
                'expected_result': 'CO BA BUOC NUA',
                'hint': f'Khóa riêng tư là: {None}',  # Will be updated
                'points': 200
            },
            4: {
                'title': 'Cấp độ 4: Mật mã AES',
                'story': 'Đây là thử thách cuối cùng! Sử dụng mật mã AES để mở khóa vị trí chính xác của kho báu!',
                'algorithm': 'aes',
                'algorithm_name': 'AES Encryption',
                'instruction': 'Nhập khóa bí mật:',
                'message': '',  # Will be generated
                'key': 'FINAL_KEY',
                'expected_result': 'CHUC MUNG BAN DA TIM THAY KHO BAU',
                'hint': 'Khóa bí mật là "FINAL_KEY"',
                'points': 250
            }
        }
        
        # Generate encrypted messages
        self._generate_encrypted_messages()
    
    def _generate_encrypted_messages(self):
        
        level1 = self.levels[1]
        level1['encrypted_message'] = self.crypto_engine.caesar_encrypt(
            level1['message'], level1['shift']
        )
        
        level2 = self.levels[2]
        level2['encrypted_message'] = self.crypto_engine.vigenere_encrypt(
            level2['message'], level2['keyword']
        )
        
        level3 = self.levels[3]
        level3['private_key'] = self.rsa_keys['private']
        level3['public_key'] = self.rsa_keys['public']
        level3['encrypted_message'] = self.crypto_engine.rsa_encrypt(
            level3['expected_result'], self.rsa_keys['public']
        )
        level3['hint'] = f'Khóa riêng tư là: {self.rsa_keys["private"]}'
        
        level4 = self.levels[4]
        level4['encrypted_message'] = self.crypto_engine.aes_encrypt(
            level4['expected_result'], level4['key'].encode()
        )
    
    def get_level_data(self, level_num):
        return self.levels.get(level_num, {})
    
    def get_algorithm_explanations(self):
        return {
            'caesar': """
            <h5>Mật mã Caesar</h5>
            <p>Mật mã Caesar là một trong những thuật toán mã hóa đơn giản nhất. Nó hoạt động bằng cách dịch chuyển mỗi chữ cái trong bảng chữ cái một số bước cố định.</p>
            <p><strong>Ví dụ:</strong> Với dịch chuyển 3, A→D, B→E, C→F</p>
            <p><strong>Cách giải:</strong> Thử các giá trị dịch chuyển từ 0-25 cho đến khi có kết quả có nghĩa.</p>
            """,
            'vigenere': """
            <h5>Mật mã Vigenère</h5>
            <p>Mật mã Vigenère sử dụng một từ khóa để mã hóa. Mỗi chữ cái trong từ khóa quy định mức độ dịch chuyển cho từng ký tự tương ứng trong thông điệp.</p>
            <p><strong>Ví dụ:</strong> Từ khóa "KEY", K=10, E=4, Y=24</p>
            <p><strong>Cách giải:</strong> Cần biết từ khóa chính xác để giải mã thành công.</p>
            """,
            'rsa': """
            <h5>Mật mã RSA</h5>
            <p>RSA là thuật toán mã hóa khóa công khai, sử dụng hai khóa: khóa công khai để mã hóa và khóa riêng tư để giải mã.</p>
            <p><strong>Nguyên lý:</strong> Dựa trên khó khăn của việc phân tích số nguyên lớn thành thừa số nguyên tố.</p>
            <p><strong>Cách giải:</strong> Cần có khóa riêng tư (n, d) để giải mã.</p>
            """,
            'aes': """
            <h5>Mật mã AES</h5>
            <p>AES (Advanced Encryption Standard) là chuẩn mã hóa hiện đại, rất an toàn và được sử dụng rộng rãi.</p>
            <p><strong>Đặc điểm:</strong> Sử dụng khóa đối xứng, cùng một khóa để mã hóa và giải mã.</p>
            <p><strong>Cách giải:</strong> Cần biết chính xác khóa bí mật để giải mã thành công.</p>
            """
        }
    
    def get_total_levels(self):
        return len(self.levels)

    def generate_practice_data(self, algorithm):
        practice_sets = {
            'caesar': [
                {
                    'message': 'XIN CHAO CAC BAN',
                    'shift': 3,
                    'hint': 'Thử với số dịch chuyển từ 1 đến 5'
                },
                {
                    'message': 'HOC LAP TRINH PYTHON',
                    'shift': 7,
                    'hint': 'Số dịch chuyển là một số nguyên tố'
                },
                {
                    'message': 'GAME MA HOA THU VI',
                    'shift': 13,
                    'hint': 'Số dịch chuyển là một nửa của 26'
                },
                {
                    'message': 'CHUC CAC BAN THANH CONG',
                    'shift': 5,
                    'hint': 'Số dịch chuyển là một số Fibonacci'
                },
                {
                    'message': 'PYTHON LA NGON NGU LAP TRINH',
                    'shift': 9,
                    'hint': 'Số dịch chuyển là bình phương của 3'
                },
                {
                    'message': 'HOC LAP TRINH KHONG KHO',
                    'shift': 15,
                    'hint': 'Số dịch chuyển là 3 nhân 5'
                },
                {
                    'message': 'CHUNG TA CUNG HOC',
                    'shift': 11,
                    'hint': 'Số dịch chuyển là một số nguyên tố'
                },
                {
                    'message': 'THANH CONG SE DEN',
                    'shift': 17,
                    'hint': 'Số dịch chuyển là một số nguyên tố'
                },
                {
                    'message': 'HOC HANH CHAM CHI',
                    'shift': 21,
                    'hint': 'Số dịch chuyển là 3 nhân 7'
                },
                {
                    'message': 'KHONG CO GI LA KHONG THE',
                    'shift': 19,
                    'hint': 'Số dịch chuyển là một số nguyên tố'
                }
            ],
            'vigenere': [
                {
                    'message': 'PYTHON LA NGON NGU LAP TRINH',
                    'keyword': 'PYTHON',
                    'hint': 'Từ khóa là tên một ngôn ngữ lập trình'
                },
                {
                    'message': 'HOC LAP TRINH KHONG KHO',
                    'keyword': 'LEARN',
                    'hint': 'Từ khóa có nghĩa là "học"'
                },
                {
                    'message': 'CHUNG TA CUNG HOC',
                    'keyword': 'CODE',
                    'hint': 'Từ khóa liên quan đến lập trình'
                },
                {
                    'message': 'THANH CONG SE DEN',
                    'keyword': 'GAME',
                    'hint': 'Từ khóa liên quan đến trò chơi'
                },
                {
                    'message': 'HOC HANH CHAM CHI',
                    'keyword': 'STUDY',
                    'hint': 'Từ khóa có nghĩa là "học tập"'
                },
                {
                    'message': 'KHONG CO GI LA KHONG THE',
                    'keyword': 'TRY',
                    'hint': 'Từ khóa có nghĩa là "thử"'
                },
                {
                    'message': 'MINH LA NGUOI HOC LAP TRINH',
                    'keyword': 'PROGRAM',
                    'hint': 'Từ khóa liên quan đến lập trình'
                },
                {
                    'message': 'PYTHON RAT DE HOC',
                    'keyword': 'EASY',
                    'hint': 'Từ khóa có nghĩa là "dễ"'
                },
                {
                    'message': 'CHUNG TA SE THANH CONG',
                    'keyword': 'SUCCESS',
                    'hint': 'Từ khóa có nghĩa là "thành công"'
                },
                {
                    'message': 'HOC LAP TRINH VUI QUA',
                    'keyword': 'FUN',
                    'hint': 'Từ khóa có nghĩa là "vui"'
                }
            ],
            'rsa': [
                {
                    'message': 'MINH LA NGUOI HOC LAP TRINH',
                    'private_key': (3233, 2753),
                    'hint': 'Khóa riêng tư là (3233, 2753)'
                },
                {
                    'message': 'PYTHON RAT DE HOC',
                    'private_key': (3127, 2011),
                    'hint': 'Khóa riêng tư là (3127, 2011)'
                },
                {
                    'message': 'CHUNG TA SE THANH CONG',
                    'private_key': (3599, 1079),
                    'hint': 'Khóa riêng tư là (3599, 1079)'
                },
                {
                    'message': 'HOC LAP TRINH VUI QUA',
                    'private_key': (4087, 2347),
                    'hint': 'Khóa riêng tư là (4087, 2347)'
                },
                {
                    'message': 'KHONG CO GI LA KHONG THE',
                    'private_key': (4693, 2293),
                    'hint': 'Khóa riêng tư là (4693, 2293)'
                },
                {
                    'message': 'MINH SE CO GANG HOC TAP',
                    'private_key': (5329, 1729),
                    'hint': 'Khóa riêng tư là (5329, 1729)'
                },
                {
                    'message': 'PYTHON LA NGON NGU TUYET VOI',
                    'private_key': (6031, 1999),
                    'hint': 'Khóa riêng tư là (6031, 1999)'
                },
                {
                    'message': 'HOC LAP TRINH KHONG KHO',
                    'private_key': (6889, 2209),
                    'hint': 'Khóa riêng tư là (6889, 2209)'
                },
                {
                    'message': 'CHUNG TA CUNG HOC',
                    'private_key': (7921, 2521),
                    'hint': 'Khóa riêng tư là (7921, 2521)'
                },
                {
                    'message': 'THANH CONG SE DEN',
                    'private_key': (9409, 2809),
                    'hint': 'Khóa riêng tư là (9409, 2809)'
                }
            ],
            'aes': [
                {
                    'message': 'WELCOME TO PYTHON',
                    'key': 'PYTHONISFUN2024',
                    'hint': 'Khóa bắt đầu bằng PYTHON'
                },
                {
                    'message': 'LEARNING IS FUN',
                    'key': 'LEARNTOCODE2024',
                    'hint': 'Khóa bắt đầu bằng LEARN'
                },
                {
                    'message': 'CODING IS AWESOME',
                    'key': 'CODEISFUN2024',
                    'hint': 'Khóa bắt đầu bằng CODE'
                },
                {
                    'message': 'PRACTICE MAKES PERFECT',
                    'key': 'PRACTICECODE2024',
                    'hint': 'Khóa bắt đầu bằng PRACTICE'
                },
                {
                    'message': 'PYTHON IS GREAT',
                    'key': 'PYTHONCODING2024',
                    'hint': 'Khóa bắt đầu bằng PYTHON'
                },
                {
                    'message': 'LEARN TO CODE',
                    'key': 'LEARNINGCODE2024',
                    'hint': 'Khóa bắt đầu bằng LEARN'
                },
                {
                    'message': 'CODE EVERY DAY',
                    'key': 'CODINGFUN2024',
                    'hint': 'Khóa bắt đầu bằng CODE'
                },
                {
                    'message': 'PRACTICE CODING',
                    'key': 'PRACTICEPYTHON2024',
                    'hint': 'Khóa bắt đầu bằng PRACTICE'
                },
                {
                    'message': 'PYTHON CODING',
                    'key': 'PYTHONLEARN2024',
                    'hint': 'Khóa bắt đầu bằng PYTHON'
                },
                {
                    'message': 'LEARN PYTHON',
                    'key': 'LEARNCODING2024',
                    'hint': 'Khóa bắt đầu bằng LEARN'
                }
            ]
        }

        import random
        practice_set = random.choice(practice_sets[algorithm])
        
        if algorithm == 'caesar':
            encrypted = self.crypto_engine.caesar_encrypt(practice_set['message'], practice_set['shift'])
            return {
                'message': practice_set['message'],
                'encrypted_message': encrypted,
                'key': practice_set['shift'],
                'hint': practice_set['hint']
            }
        elif algorithm == 'vigenere':
            encrypted = self.crypto_engine.vigenere_encrypt(practice_set['message'], practice_set['keyword'])
            return {
                'message': practice_set['message'],
                'encrypted_message': encrypted,
                'key': practice_set['keyword'],
                'hint': practice_set['hint']
            }
        elif algorithm == 'rsa':
            encrypted = self.crypto_engine.rsa_encrypt(practice_set['message'], (practice_set['private_key'][0], 65537))
            return {
                'message': practice_set['message'],
                'encrypted_message': encrypted,
                'key': practice_set['private_key'],
                'hint': practice_set['hint']
            }
        elif algorithm == 'aes':
            encrypted = self.crypto_engine.aes_encrypt(practice_set['message'], practice_set['key'].encode())
            return {
                'message': practice_set['message'],
                'encrypted_message': encrypted,
                'key': practice_set['key'],
                'hint': practice_set['hint']
            }
