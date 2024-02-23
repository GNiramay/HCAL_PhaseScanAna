// Script to make stack plot of the TDC code, from a 2D histogram of TDC vs shift.
// To compile: g++ -o MakeTDCStack.app MakeTDCStack.C `root-config --cflags --glibs`
// To execute: ./MakeTDCStack.app <input root file> <output png file>

#include<iostream>
#include"TCanvas.h"
#include"TH2F.h"
#include"THStack.h"
#include"TFile.h"
using namespace std;

int main(int argc,char** argv)
{
  // cout<<argv[1]<<"\t"<<argv[2]<<endl;
  TFile* tf = new TFile(argv[1],"READ");
  TH2F* hist = (TH2F*)tf->Get("h2TDCvTShift");
  // hist->Print("all");
  THStack* hs = new THStack();
  // auto hStat = hist->ProjectionX();
  // auto hStat = hist->ProjectionX("hStat",0,5);
  // hStat->Print("all");
  for(int i=0;i<4;i++){
    auto htemp = hist->ProjectionX(Form("hTDC%d",i),i+1,i+2);
    htemp->SetTitle(Form("TDC %d; time shift [ns]",i));
    htemp->SetFillColor(i+2);
    htemp->SetLineColor(1);
    // htemp->Print("all");

    // Scale each shift
    for(int j = 1;j<htemp->GetNbinsX()-1;j++){
      Double_t nTotEvt = 0;
      for(int k=01;k<5;k++) nTotEvt += hist->GetBinContent(j,k);
      cout<<j<<"\t"<<nTotEvt<<"\t"<<htemp->GetBinContent(j)<<endl;
      // htemp->SetBinContent(j,0);
      if(nTotEvt !=0) htemp->SetBinContent(j,htemp->GetBinContent(j)/nTotEvt);
      // if(nTotEvt !=0) htemp->Fill(j,htemp->GetBinContent(j)/nTotEvt);
      cout<<j<<"\t"<<nTotEvt<<"\t"<<htemp->GetBinContent(j)<<endl;
      //   if(hStat->GetBinContent(j) != 0)
      // 	htemp->SetBinContent(j,htemp->GetBinContent(j)/hStat->GetBinContent(j));
    }
    hs->Add(htemp);    
  }

  TCanvas* tc = new TCanvas("aa","bb",800,600);
  hs->Draw("hist");
  hs->SetTitle(hist->GetTitle());
  tc->BuildLegend(.8,.7,.9,.9);
  tc->SaveAs(argv[2]);
}
