#  PART A
#  each variable is in units of 100g 
#  minimize kcal:  21*tom + 16*lett + 40*spin + 41*carr + 585*sun + 120*tofu + 
#               164*chick + 884*oil 
#  st:  all >= 0
#       at least 15g protein:
#       0.85*tom + 1.62*lett + 2.86*spin + 0.93*carr + 23.4*sun + 16.0*tofu + 
#               9.0*chick + 0.0*oil >= 15

#       btw 2 and 8g fat
#       0.33*tom + .20*lett + .39*spin + 0.24*carr + 48.7*sun + 5.0*tofu + 
#               2.6*chick + 100.0*oil >= 2 
#       0.33*tom + .20*lett + .39*spin + 0.24*carr + 48.7*sun + 5.0*tofu + 
#               2.6*chick + 100.0*oil <= 8 
#       
#       at least 4g carbs
#       4.64*tom + 2.37*lett + 3.63*spin + 9.58*carr + 15.0*sun + 3.0*tofu + 
#               27.0*chick + 0.0*oil >= 4 
#
#       at most 200mg sodium 
#       .009*tom + .028*lett + .065*spin + .069*carr + .0038*sun + .120*tofu + 
#               .078*chick + 0.0*oil <= .200 
#
#       at least 40% leafy greens by weight
#       lett + spin >= 0.4*(tom + lett + spin + carr + sun + tofu +
#                           chick + oil)
