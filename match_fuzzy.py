from thefuzz import fuzz


def return_best_fuzz_match(x,df):

    max_found=0
    cols_and_scores={}
    found=''

    for col in df.columns:
        fuzz_score=fuzz.ratio(x,col.lower().replace(' ',''))
        cols_and_scores[col]=fuzz_score
        max_found=max(max_found,fuzz_score)
        

    for key in cols_and_scores:
        if cols_and_scores[key]==max_found:
            found=key
            break
    return found, max_found


if '__name__'=='__main__':
    return_best_fuzz_match(x,df)

