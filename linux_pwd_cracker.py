import crypt 
import sys

def crack_pwd(user, pwd_dictionary, shadow_file):
    """Tries to authenticate a user.
    Returns True if the authentication succeeds, else the reason
    (string) is returned."""
    is_user_available = False
    encrypted_pwd = ''
    with open(shadow_file, 'rb') as f:
        for each_line in f:
            each_line = each_line.replace('\n', '')
            if user in each_line:
                is_user_available = True
                encrypted_pwd = each_line.split(':')[1]
                break
        if not is_user_available:
            print "No user found with username", user
            sys.exit(1)
    
    if encrypted_pwd in ["NP", "!", "", None]:
        print "User", user, "has no password"
        sys.exit(1)

    if encrypted_pwd in ["LK", "*"]:
        print "Account is locked"
        sys.exit(1)

    if encrypted_pwd == "!!":
        print "Password has expired"
        sys.exit(1)

    with open(pwd_dictionary, 'rb') as f:
        for each_pass in f:
            each_pass = each_pass.replace('\n', '')
            if crypt.crypt(each_pass, encrypted_pwd) == encrypted_pwd:
                print "Password found: ", each_pass
                sys.exit(1)
        print "Password not found"

if __name__ == "__main__":
    username = raw_input("Username: ")
    pwd_dictionary = raw_input("Password dictionary file path: ")
    shadow_file = raw_input("Linux password file path(hint /etc/shadow) : ")	#pass /etc/shadow
    crack_pwd(username, pwd_dictionary, shadow_file)
    
