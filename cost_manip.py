import time
def main0(BaselineFP,OtherFPs):
    BLSentAv,BLWdAv=average_sent_word_cost(BaselineFP)
    print(BLSentAv);print(BLWdAv)
    for FP in OtherFPs:
        Sents=pick_positive_distances(FP,BLSentAv,BLWdAv)
        for Sent in Sents:
            print(Sent)
            time.sleep(3)

def pick_positive_distances(FP,BLSentAv,BLWdAv):
    Sents=[]
    for SentCntr,SentStat in enumerate(generate_sentstat(FP)):
        if not SentStat:
            break
        SentCost=SentStat[-1][-1]
        SentCostDiff=SentCost-BLSentAv
        if SentCostDiff>0:
            WdStrs=[];WdCosts=[]
            for Cntr,WdTuple in enumerate(SentStat):
                WdStrs.append(WdTuple[0])
                WdCostDiff=WdTuple[-1]-BLWdAv
                if WdCostDiff>0:
                    WdCosts.append((Cntr,WdCostDiff))
            Sents.append((SentCntr+1,WdStrs,SentCost,WdCosts,SentCostDiff))
        
    return Sents
            

def generate_sentstat(FP):
    with open(FP) as FSr:
        SentStat=[]
        for LiNe in FSr:
            if LiNe=='EOS\n':
                yield SentStat
                SentStat=[]
            else:
                LineEls=LiNe.strip().split()
                SF,Fts,UnitC,CxtC,Cost,CumCost=LineEls
                SentStat.append((SF,Fts,int(UnitC),int(CxtC),int(Cost),int(CumCost)))
            

def average_sent_word_cost(FP):
    WdCumCost=0;SentCumCost=0
    WdCnt=0
    for (Cntr,SentStat) in enumerate(generate_sentstat(FP)):
        SentCnt=Cntr+1
        WdCnt+=len(SentStat)
        WdCosts=[ Tuple[-2] for Tuple in SentStat ]
        WdCumCost+=sum(WdCosts)
        SentCumCost+=SentStat[-1][-1]
    return SentCumCost/SentCnt,WdCumCost/WdCnt
    

def main():
    import glob
    FPs=glob.glob('sampledata/*.mecabc')
    BaselineFPs=[FP for FP in FPs if 'tk' in FP][0]
    OtherFPs=[FP for FP in FPs if 'tk' not in FP]
    main0(BaselineFPs,OtherFPs)


if __name__=='__main__':
    main()


    
