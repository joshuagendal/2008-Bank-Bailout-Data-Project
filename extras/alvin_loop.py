a = Bailout.objects.all()
for n, i in enumerate(a):
    try:
        i.vote_1 = df['vote1'][n]
        i.save()
    except:
        print "Wrong"