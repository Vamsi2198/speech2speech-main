
import random


def simulate_two_months(df,num_sims,column_chosen,cat_col,unit):
    
    map_search={'January':'February','February':'March','March':'April','April':'May','May':'June',\
            'June':'July','July':'August','August':'September','September':'October',\
            'October':'November','November':'December'}
    
    count=0
    
    total_occurances_searched=0
    total_occurances_found=0
    
    increases=[]
    
    while count<=num_sims:
        
        key_chosen=random.choice(list(map_search.keys()))
        val_mapped=map_search[key_chosen]
        
        slashed_df_month1=df[(df['Month']==key_chosen) & (df[cat_col]==unit)]
        
        val_month1=random.choice(slashed_df_month1[column_chosen].values)
        val_month1_chosen=list(slashed_df_month1[column_chosen].values).index(val_month1)
        
        
        slashed_df_next_month=df[(df['Month']==val_mapped) & (df[cat_col]==unit)]
        val_next_month1=list(slashed_df_next_month[column_chosen].values)[val_month1_chosen]
        
        
        if val_month1<val_next_month1:
            total_occurances_found+=1
            
            perc_inc=((val_next_month1-val_month1)/abs(val_month1))*100
            increases.append(perc_inc)
            
            print(f'{val_month1} {val_next_month1}')
            
        total_occurances_searched+=1
        count+=1
            
    return total_occurances_found/total_occurances_searched,increases


if '__name__'=='__main__':
    simulate_two_months(df,num_sims)

