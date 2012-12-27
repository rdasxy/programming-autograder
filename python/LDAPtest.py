import ldap


l = ldap.initialize("ldap://ldap.umkc.edu:636/")
l.set_option(ldap.OPT_REFERRALS, 0)

print l.simple_bind("CN=spatzs,OU=Users,DC=kc,DC=umkc,DC=edu","password")

    
