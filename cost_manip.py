def generate_sentstat(FP):
    with open(FP) as FSr:
        SentStat=[]
        for LiNe in FSr:
            if LiNe=='EOS\n':
                yield SentStat
            LineEls=LiNe.strip().split()
            SF,Fts,UnitC,CxtC,Cost,CumCost=LineEls
            SentStat.append({SF:(Fts,int(UnitC),int(CxtC),int(Cost),int(CumCost))})
            

def average_sent_cost():
                            

def average_word_cost():
    
