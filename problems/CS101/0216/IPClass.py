class IP(object):
        def __init__(self, Addy='Undefined'):
                self.Address = Addy

        def Domain(self):
                if self.Address.startswith('134.193.'):
                        return 'UMKC'
                else:
                        return 'Not UMKC'
                
