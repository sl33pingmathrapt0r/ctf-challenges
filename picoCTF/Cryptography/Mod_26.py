"""
This challenge implements ROT13. This is a 
Caesar Cipher of rotating 13 places. While utterly
useless, it has a cool property of being 
invertible. i.e. ROT13( ROT13( A ) ) == A;

Retrieve the flag from:
cvpbPGS{arkg_gvzr_V'yy_gel_2_ebhaqf_bs_ebg13_nSkgmDJE}
"""

rot13_char= lambda char: char if not char.isalpha() else (  chr( ( (( ord(char)-97 ) +13) %26) +97 ) if char.islower() else chr( ( (( ord(char)-65) +13) %26) + 65 )  )
rot13= lambda flag: ''.join([rot13_char(x) for x in flag])

print(rot13("cvpbPGS{arkg_gvzr_V'yy_gel_2_ebhaqf_bs_ebg13_nSkgmDJE}"))
