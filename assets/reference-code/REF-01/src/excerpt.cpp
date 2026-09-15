// cardview.h
class CCardView : public CView
{
protected:
    CCardView();
    DECLARE_DYNCREATE(CCardView)

public:
    CCardDoc* GetDocument();
    virtual void OnDraw(CDC* pDC);

protected:
    //{{AFX_MSG(CCardView)
    afx_msg void OnLButtonDown(UINT nFlags, CPoint point);
    afx_msg void OnGameDeal();
    afx_msg void OnUpdateGameDeal(CCmdUI* pCmdUI);
    //}}AFX_MSG
    DECLARE_MESSAGE_MAP()
};

// cardview.cpp
IMPLEMENT_DYNCREATE(CCardView, CView)

BEGIN_MESSAGE_MAP(CCardView, CView)
    //{{AFX_MSG_MAP(CCardView)
    ON_WM_LBUTTONDOWN()
    ON_COMMAND(ID_GAME_DEAL, OnGameDeal)
    ON_UPDATE_COMMAND_UI(ID_GAME_DEAL, OnUpdateGameDeal)
    //}}AFX_MSG_MAP
END_MESSAGE_MAP()

void CCardView::OnLButtonDown(UINT nFlags, CPoint point)
{
    GetDocument()->FlipNextCard();
    Invalidate();
    CView::OnLButtonDown(nFlags, point);
}

void CCardView::OnGameDeal()
{
    GetDocument()->Deal();
    Invalidate();
}

void CCardView::OnUpdateGameDeal(CCmdUI* pCmdUI)
{
    pCmdUI->Enable(!GetDocument()->IsDealt());
}
