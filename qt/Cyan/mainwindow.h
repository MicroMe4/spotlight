#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QString>
#include <QMessageBox>
#include <QUrl>
#include <QFile>
#include <QFileInfo>
#include <QtWebKit/QtWebKit>
#include <QtWebKitWidgets/QWebFrame>
#include <QtWebKitWidgets/QWebView>
#include <QtMath>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
private slots:
    void slotExecJScrpitQT();
    void on_actionLoad_Data_triggered();
    void on_actionRefresh_triggered();
    void on_actionFile_API_Test_triggered();
    void on_actionThis_Program_triggered();
    void on_actionStreet_Map_triggered();
    void on_actionSatellite_Map_triggered();

private:
    const static quint8 WGS84=0;
    const static quint8 GCJ02=1;
    const static quint8 BD09=2;
    const static quint8 ROUGH=3;
    const static quint8 PERCIOUS=4;
    Ui::MainWindow *ui;
    QString qstrDir;
    QUrl pageUrl;
    QString fileLoc;
    std::vector<qreal> LatiVec;
    std::vector<qreal> LngtVec;
    QUrl getUrl();
    QString getDataLocation();
    quint8 CoDataType;
    void loadCoordiante(bool);
    void init();
};

#endif // MAINWINDOW_H
