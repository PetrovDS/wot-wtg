#ifndef WRPARSER_H
#define WRPARSER_H

#include <QWidget>

namespace Ui {
class WRParser;
}

class WRParser : public QWidget
{
    Q_OBJECT

public:
    explicit WRParser(QWidget *parent = 0);
    ~WRParser();

private:
    Ui::WRParser *ui;
};

#endif // WRPARSER_H
