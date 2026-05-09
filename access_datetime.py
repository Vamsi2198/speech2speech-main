from match_fuzzy import return_best_fuzz_match


def access_datetime(df):

    """
    using fuzzy algorithm to automatically detect datetime columns

    """

    month_match,score_m=return_best_fuzz_match('month',df)
    year_match,score_y=return_best_fuzz_match('year',df)
    date_match,score_d=return_best_fuzz_match('date',df)

    return month_match,year_match,date_match,score_m,score_y,score_d

if '__name__'=='__main__':
    access_datetime(df)
    






    