"""
A simpler interface for GnuPGInterface. I *think* I
(michal) wrote this, but I'm not 100% sure. In any
case it's based on the docstrings in GnuPGInterface
"""
try:
    import GnuPGInterface
    BaseClass = GnuPGInterface.GnuPG    
except:
    GnuPGInterface = None
    BaseClass = object
    

class GnuPG(BaseClass):
    def __init__(self):
        assert GnuPGInterface, "can't do this without GnuPGInterface!!"
        GnuPGInterface.GnuPG.__init__(self)
        self.setup_my_options()

    def waitfor(self, proc):
        try:
            proc.wait()
        except:
            raise IOError("GnuPG failed:\n" + proc.handles["stderr"].read())
        
    def setup_my_options(self):
        self.options.armor = 1
        self.options.meta_interactive = 0
        self.options.extra_args.append('--no-secmem-warning')
        
    def encrypt_string(self, string, recipients):
        self.options.recipients = recipients   # a list!
        proc = self.run(['--encrypt'], create_fhs=['stdin', 'stdout', 'stderr'])
        proc.handles['stdin'].write(string)
        proc.handles['stdin'].close()
        output = proc.handles['stdout'].read()
        proc.handles['stdout'].close()
        self.waitfor(proc)
        return output
    

    def decrypt_string(self, ciphertext, passphrase):
        self.passphrase = passphrase
        p = self.run(['--decrypt', "--quiet"],
                     create_fhs=['stdin','stdout','stderr'])
        p.handles['stdin'].write(ciphertext)
        p.handles['stdin'].close()
        res = p.handles['stdout'].read()
        p.handles['stderr'].close()
        p.handles['stdout'].close()
        self.waitfor(p)
        self.passphrase = None
        return res
