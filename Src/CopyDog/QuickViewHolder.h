#ifndef QUICKVIEWHOLDER_H
#define QUICKVIEWHOLDER_H

#include <QQuickItem>

class QuickViewHolder
{
public:
    QuickViewHolder();
    QQuickItem * getView() { return view ; }
    void setView(QQuickItem * tempView) { view = tempView ; }

private:

    QQuickItem * view;
};


#endif // QUICKVIEWHOLDER_H
