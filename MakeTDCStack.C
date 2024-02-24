// Script to make stack plot of the TDC code, from a 2D histogram of TDC vs shift.
// To compile: g++ -o MakeTDCStack.app MakeTDCStack.C `root-config --cflags --glibs`
// To execute: ./MakeTDCStack.app <input root file> <output png file>

#include<iostream>
#include"TCanvas.h"
#include"TH2F.h"
#include"TH1F.h"
#include"THStack.h"
#include"TFile.h"
using namespace std;
// THStack* Trial1(TH2F*);
THStack* Trial2(TH2F*);
TString TDCInfo[4] = {"Prompt","Slight delay","Delayed","No TDC"};

int main(int argc,char** argv)
{
  TFile* tf = new TFile(argv[1],"READ");
  TH2F* hist = (TH2F*)tf->Get("h2TDCvTShift");
  // THStack* hs = new THStack();
  // TH1F* hTDC[4] = {
  //   new TH1F("hTDC0","",32,-10.5,21.5),
  //   new TH1F("hTDC1","",32,-10.5,21.5),
  //   new TH1F("hTDC2","",32,-10.5,21.5),
  //   new TH1F("hTDC3","",32,-10.5,21.5)};
  
  // int nxbins = hist->GetNbinsX();
  // int nybins = hist->GetNbinsY();
  // Double_t* nTotEvt = new Double_t[nxbins];

  // for(int bx = 1;bx<=nxbins;bx++){
  //   Double_t temp = 0;
  //   for(int by = 1;by<=nybins;by++)
  //     temp += hist->GetBinContent(hist->GetBin(bx,by));
  //   nTotEvt[bx-1] = temp;
  // }

  // for(int by = 1;by<=nybins;by++){
  //   hTDC[by-1]->SetTitle(Form("TDC %d (%s); time shift [ns]",by-1,TDCInfo[by-1].Data()));
  //   hTDC[by-1]->SetFillColor(by+1);
  //   hTDC[by-1]->SetLineColor(1);
  //   for(int bx = 1;bx<=nxbins;bx++){
  //     if(nTotEvt[bx-1]!=0)
  // 	hTDC[by-1]->SetBinContent(bx-1,hist->GetBinContent(hist->GetBin(bx,by))/nTotEvt[bx-1]);
  //   }
  //   hs->Add(hTDC[by-1]);
  // }

  auto hs = Trial2(hist);

  TCanvas* tc = new TCanvas("aa","bb",800,600);
  hs->Draw("hist");
  // Some formatting
  hs->SetTitle(""+(TString)hist->GetTitle()+";time shift [ns];fraction of events");
  tc->BuildLegend(.7,.7,.9,.9);
  hs->SetMaximum(1);

  // Save png
  tc->SaveAs(argv[2]);
  delete tc;
  delete hs;
  tf->Close();
  return 0;
}

// THStack* Trial1(TH2F* hist)
// {
//   THStack* hs = new THStack();
//   TH1F* hTDC[4] = {
//     new TH1F("hTDC0","",32,-10.5,21.5),
//     new TH1F("hTDC1","",32,-10.5,21.5),
//     new TH1F("hTDC2","",32,-10.5,21.5),
//     new TH1F("hTDC3","",32,-10.5,21.5)};
  
//   int nxbins = hist->GetNbinsX();
//   int nybins = hist->GetNbinsY();
//   Double_t* nTotEvt = new Double_t[nxbins];

//   for(int bx = 1;bx<=nxbins;bx++){
//     Double_t temp = 0;
//     for(int by = 1;by<=nybins;by++)
//       temp += hist->GetBinContent(hist->GetBin(bx,by));
//     nTotEvt[bx-1] = temp;
//   }

//   for(int by = 1;by<=nybins;by++){
//     hTDC[by-1]->SetTitle(Form("TDC %d (%s); time shift [ns]",by-1,TDCInfo[by-1].Data()));
//     hTDC[by-1]->SetFillColor(by+1);
//     hTDC[by-1]->SetLineColor(1);
//     for(int bx = 1;bx<=nxbins;bx++){
//       if(nTotEvt[bx-1]!=0)
// 	hTDC[by-1]->SetBinContent(bx-1,hist->GetBinContent(hist->GetBin(bx,by))/nTotEvt[bx-1]);
//     }
//     hs->Add(hTDC[by-1]);
//   }
//   return hs;
// }

THStack* Trial2(TH2F* hist_)
{
  THStack* hs_ = new THStack();
  auto hTotEvt = hist_->ProjectionX();
  int nxbins = hist_->GetNbinsX();
  int nybins = hist_->GetNbinsY();

  TH1F* hTDC[4] = {
    new TH1F("hTDC0","",nxbins,hTotEvt->GetBinLowEdge(0),hTotEvt->GetBinLowEdge(nxbins)),
    new TH1F("hTDC1","",nxbins,hTotEvt->GetBinLowEdge(0),hTotEvt->GetBinLowEdge(nxbins)),
    new TH1F("hTDC2","",nxbins,hTotEvt->GetBinLowEdge(0),hTotEvt->GetBinLowEdge(nxbins)),
    new TH1F("hTDC3","",nxbins,hTotEvt->GetBinLowEdge(0),hTotEvt->GetBinLowEdge(nxbins))};
  

  for(int by = 1;by<=nybins;by++){
    hTDC[by-1]->SetTitle(Form("TDC %d (%s); time shift [ns]",by-1,TDCInfo[by-1].Data()));
    hTDC[by-1]->SetFillColor(by+1);
    hTDC[by-1]->SetLineColor(1);

    for(int bx = 0;bx<nxbins;bx++)
      if(hTotEvt->GetBinContent(bx+1)!=0)
	hTDC[by-1]->SetBinContent(bx,hist_->GetBinContent(hist_->GetBin(bx+1,by))/hTotEvt->GetBinContent(bx+1));

    hs_->Add(hTDC[by-1]);
  }
  return hs_;
}
