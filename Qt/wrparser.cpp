#include "wrparser.h"
#include "ui_wrparser.h"

WRParser::WRParser(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::WRParser)
{
    ui->setupUi(this);
}

WRParser::~WRParser()
{
    delete ui;
}
