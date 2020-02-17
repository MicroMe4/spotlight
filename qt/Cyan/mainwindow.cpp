#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    this->CoDataType=3;
    this->qstrDir=QCoreApplication::applicationDirPath();
    this->pageUrl=this->getUrl();
    this->fileLoc=this->getDataLocation();
    qDebug() << "Following is the detail of enviorment:";
    qDebug() << "Respond of QCoreApplication::applicationDirPath():" + this->qstrDir;
    qDebug() << "Respond of GetURL of localfile:" + this->pageUrl.toString();
    qDebug() << "Respond of Get Location:" + this->fileLoc;
    ui->webView->load(this->pageUrl);
    //连接开始。连接的时候确认完全加载完毕。
    connect(ui->webView->page()->mainFrame(),SIGNAL(javaScriptWindowObjectCleared()),this,SLOT(slotExecJScrpitQT()));
}

MainWindow::~MainWindow()
{
    delete ui;
}

//将JS和Qt连接起来。没事的话就不要改了
void MainWindow::slotExecJScrpitQT(){
    ui->webView->page()->mainFrame()->addToJavaScriptWindowObject("localhost",this);
}


void MainWindow::on_actionLoad_Data_triggered()
{
    this->LatiVec.clear();
    this->LngtVec.clear();
    this->loadCoordiante(false);
    QJsonArray NumLat,NumLng;
    for(std::vector<qreal>::size_type i=0;i<this->LatiVec.size();i++){
        qDebug() << "Latitude analyze:" << std::to_string(this->LatiVec.at(i)).c_str();
        NumLat.append(this->LatiVec.at(i));
        NumLng.append(this->LngtVec.at(i));
    }
    QJsonDocument docLat,docLng;
    QByteArray baLat,baLng;
    docLat.setArray(NumLat);
    docLng.setArray(NumLng);
    baLat=docLat.toJson(QJsonDocument::Compact);
    baLng=docLng.toJson(QJsonDocument::Compact);
    QString strLat(baLat);
    QString strLng(baLng);
    QWebFrame *webframe=ui->webView->page()->mainFrame();
    QString runcmd = QString("showarray(\"%1\",\"%2\")").arg(strLat).arg(strLng);
    webframe->evaluateJavaScript(runcmd);
    webframe=nullptr; //always need no useless pointer
    free(webframe);
}

void MainWindow::loadCoordiante(bool isShowSuccess=true){
    QFile file(this->fileLoc);
    QFileInfo fileInfo;
    fileInfo.setFile(file);
    std::vector<QString> strList;
    if(!file.exists()){
        QMessageBox::critical(nullptr,"No Such File Error","No File Named "+ fileInfo.fileName() + " exists, please put your coordinate file in this location:",QMessageBox::Ok,QMessageBox::Ok); //无法找到文件的提示。
        //qDebug() << "File Path=" + fileInfo.absoluteFilePath();
        //qDebug() << "QSTRDIR=" + this->qstrDir;
    }
    else {
        file.open(QIODevice::ReadOnly|QIODevice::Text); //no damange to data.
        if(!file.isOpen()){
            QMessageBox::critical(nullptr,"read Permission Error","you have no read permission to file"+ file.fileName() + " . you should change a directory to reoperate.",QMessageBox::Ok,QMessageBox::Ok); //无读权限情况下的提示
        }
        if(isShowSuccess){
            QMessageBox::information(nullptr,"File Load Successful!","Find File. Now Loading...",QMessageBox::Ok,QMessageBox::Ok); //提示读取成功。
        }
        QString readLineStr;
        QStringList coordStrList;
        while(!file.atEnd()){
            readLineStr=file.readLine();
            if(readLineStr.contains(',')){
                strList.push_back(readLineStr);
                //qDebug() << readLineStr;
            }
        }
        for(auto operateStr:strList){
            coordStrList=operateStr.split(',');
            //经度在前的写法
            //qDebug() << coordStrList.at(1) << "," << coordStrList.at(0);
            //qDebug() << "After Remove coordStrList's LineChanger:" << QString(std::to_string(coordStrList.at(1).toDouble()).c_str());
            this->LngtVec.push_back(coordStrList.at(1).toDouble());
            this->LatiVec.push_back(coordStrList.at(0).toDouble());
            //纬度在前的写法
            //this->LngtVec.push_back(coordStrList.at(0).toDouble());
            //this->LatiVec.push_back(coordStrList.at(1).toDouble());
        }
        file.close();
    }
}

void MainWindow::on_actionRefresh_triggered()
{
    ui->webView->load(this->pageUrl);
}

void MainWindow::on_actionFile_API_Test_triggered()
{
    this->loadCoordiante();
}

QUrl MainWindow::getUrl(){
    return QUrl("file:///"+this->qstrDir+"/index.html"); // 重写网页名称的话是在这儿。
}

QString MainWindow::getDataLocation(){
    return QString(this->qstrDir+"/co.txt"); //要重写地址的话在这个地方写哦。
}

void MainWindow::on_actionThis_Program_triggered()
{
    QMessageBox::information(nullptr,"About This Program","This is Written in Qt 5.9 with QtWebkit Support.",QMessageBox::Ok,QMessageBox::Ok);
}

void MainWindow::on_actionStreet_Map_triggered()
{
    QWebFrame *webFrame=ui->webView->page()->mainFrame();
    webFrame->evaluateJavaScript(QString("showStreetMap()"));
    webFrame=nullptr;
    free(webFrame);
}

void MainWindow::on_actionSatellite_Map_triggered()
{
    QWebFrame *webFrame=ui->webView->page()->mainFrame();
    webFrame->evaluateJavaScript(QString("showSatelliteMap()"));
    webFrame=nullptr;
    free(webFrame);
}
