import streamlit as st
import random

def find_consecutive_three_increase(arra,arra_yr,arra_mnth)->str:
    
    flag_print=0
    
    for val in range(len(arra)):

        if val>=len(arra)-3:
            
            
            
            word_choice=['Further','Morover','Henceforth','Hereafter','Also']
            
            word_chosen=random.choice(word_choice)
            
            num1=arra[len(arra)-3]
            num2=arra[len(arra)-2]
            num3=arra[len(arra)-1]
            
            if num1<num2 and num2<num3:
               
                 
                
                if num1<0 and num3>0:
                    increase_notice=round(abs(((num3-num1)/num1)*100),2)
                elif num1<0 and num3<0:
                    increase_notice=round(abs(((num3-num1)/num1)*100),2)
                else:
                    increase_notice=((num3-num1)/num1)*100
                    increase_notice=round(increase_notice,2)


                
                
                if flag_print==0 and increase_notice>0:
                    st.markdown(f'We have noticed a :green[consecutive increase in Amount for 3 months] from {arra_mnth[len(arra)-3]} {arra_yr[len(arra)-3]} to {arra_mnth[len(arra)-1]} {arra_yr[len(arra)-1]} by a total :green[{increase_notice}%].')
                    flag_print=1
                
                elif flag_print==1 and increase_notice>0:
                    st.markdown(f'{word_chosen}, continuous increases were also found from {arra_mnth[len(arra)-3]} {arra_yr[len(arra)-3]} to {arra_mnth[len(arra)-1]} {arra_yr[len(arra)-1]} by a total :green[{increase_notice}%].')
                break
            else:
                pass
        else:
            num1=arra[val]
            num2=arra[val+1]
            num3=arra[val+2]
            
            word_choice=['Further','Morover','Henceforth','Hereafter','Also']
            
            word_chosen=random.choice(word_choice)
            
            
            if num1<num2 and num2<num3:


                if num1<0 and num3>0:
                    increase_notice=round(abs(((num3-num1)/num1)*100),2)
                elif num1<0 and num3<0:
                    increase_notice=round(abs(((num3-num1)/num1)*100),2)
                else:
                    increase_notice=((num3-num1)/num1)*100
                    increase_notice=round(increase_notice,2)


                
               
                
                if flag_print==0 and increase_notice>0:
                    st.markdown(f'We have noticed a consecutive increase in Amount for 3 months from {arra_mnth[val]} {arra_yr[val]} to {arra_mnth[val+2]} {arra_yr[val+2]} by a total :green[{increase_notice}%].')
                    flag_print=1
                elif flag_print==1 and increase_notice>0:
                    st.markdown(f'{word_chosen}, continuous increases were also found from {arra_mnth[val]} {arra_yr[val]} to {arra_mnth[val+2]} {arra_yr[val+2]} by a total :green[{increase_notice}%].')
                