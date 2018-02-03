import time,os,sys

def main0(BaselineFP,OtherFPs):
 #   BLSentAv,BLWdAv=average_sent_word_cost(BaselineFP)
  #  print(BLSentAv);print(BLWdAv)
    BLSentAv=-39978
    BLWdAv=-1762
    for FP in OtherFPs:
        Sents=pick_positive_distances(FP,BLSentAv,BLWdAv)
        AllSentsCnt=len(Sents)
        Sents1=[];Sents2=[];Sents3=[];Sents4=[]
        for Sent in Sents:
            if Sent[-1]<10000:
                Sents1.append(Sent)
            elif Sent[-1]<50000:
                Sents2.append(Sent)
            elif Sent[-1]<90000:
                Sents3.append(Sent)
            else:
                Sents4.append(Sent)
        Sents=(Sents1,Sents2,Sents3,Sents4)
        for Cntr,SentSet in enumerate(Sents):
            CatSentsCnt=len(SentSet)
            print(FP)
            print('\nCategory '+str(Cntr+1))
            print(str(CatSentsCnt)+' or '+str(CatSentsCnt/AllSentsCnt*100)+'%')
            time.sleep(3)
            if Cntr==0 or Cntr==3:
                for Cntr,Sent in enumerate(SentSet):
                    print(Sent)
                    time.sleep(1)

def pick_positive_distances(FP,BLSentAv,BLWdAv):
    Sents=[]
    Buffer=-10000
    for SentCntr,SentStat in enumerate(generate_sentstat(FP)):
        if not SentStat:
            break
        SentCost=SentStat[-1][-1]
        SentCostDiff=round(SentCost-BLSentAv,2)
        if SentCostDiff>Buffer:
            WdStrs=[];WdCosts=[]
            for Cntr,WdTuple in enumerate(SentStat):
                WdStrs.append(WdTuple[0])
                WdCostDiff=round(WdTuple[-1]-BLWdAv,2)
                if WdCostDiff>Buffer:
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
    import argparse,glob
    Psr=argparse.ArgumentParser()
    Psr.add_argument('-b','--baseline-fp',required=True)
    Psr.add_argument('-t','--target-dir',required=True)
    Args=Psr.parse_args()
    TgtFPs=glob.glob(os.path.join(Args.target_dir,'*.mecabc'))
    if TgtFPs and os.path.isfile(Args.baseline_fp):
        main0(Args.baseline_fp,TgtFPs)
    else:
        sys.exit('either tgt or baseline fp does not exist')


if __name__=='__main__':
    main()


    
