for n, i in enumerate(g):
    try:
        i.vote_1 = df['vote1'][n]
        i.save()
    except:
        print "Wrong"