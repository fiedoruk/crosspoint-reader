#include <ArduinoJson.h>
#include <cstring>
#include <cstdio>
#include <cstdarg>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using String = std::string;
std::string logline;
void logerr(const char* fmt, ...) { char buf[1024]; va_list a; va_start(a,fmt); vsnprintf(buf,sizeof(buf),fmt,a); va_end(a); logline=buf; }
#define LOG_ERR(tag, ...) logerr(__VA_ARGS__)
enum class StrId { STR_DOWNLOAD_FAILED };
struct { const char* get(StrId) { return "Download failed"; } } I18N;
enum { STR_ERROR_MSG, STR_TAP_TO_RETRY, ACTION_CANCEL };
const char* tr(int id) { return id==STR_ERROR_MSG ? "Error" : "Tap to retry"; }
namespace HttpDownloader { enum DownloadError {OK, ABORTED, HTTP_ERROR}; }
struct UiScreen { struct Theme { int bodyText; }; Theme theme() {return {};} void centeredText(const char*,int) {} };
struct Line {const char* text; bool bold=false;};
std::vector<std::string> rendered;
void catalogCenteredBlock(UiScreen&, std::initializer_list<Line> lines) {rendered.clear(); for(auto l:lines) rendered.emplace_back(l.text);}
void catalogDownloadScreen(UiScreen&,const char*,size_t,size_t,int) {}
struct CatalogActivity {
 enum class State { DOWNLOADING, ERROR, CHECK_WIFI, WIFI_SELECTION, SEARCH_INPUT, LOADING, OTHER };
 State state=State::OTHER; std::string errorMessage,statusMessage; size_t downloadProgress=0,downloadTotal=0; bool goHomeAfterCancel=false; bool updated=false,home=false,finished=false;
 struct { bool touch=false; bool hasTouch() {return touch;} } mappedInput;
 void requestUpdate() {updated=true;} void onGoHome(){home=true;} void downloadFinished(bool){finished=true;}
 void fail(StrId,const std::string& detail={}); void finishDownload(HttpDownloader::DownloadError,const std::string& detail={}); bool buildStatusScreen(UiScreen&,bool,bool);
};
#include "actual.inc"
void check(bool b,const char* name) {if(!b){std::cerr<<"FAIL "<<name<<"\n"; std::exit(1);} std::cout<<"PASS "<<name<<"\n";}
int main() {
 for(int code : {401,403,404,422,429,503}) {auto d=httpFailureDetail(code,"{\"error\":\"Example\"}"); check(d=="HTTP "+std::to_string(code)+": Example","HTTP status with error");}
 check(httpFailureDetail(422,"{\"error\":\"\",\"message\":\"Try later\"}")=="HTTP 422: Try later","empty error falls back to message");
 check(httpFailureDetail(422,"{\"message\":\"Try later\"}")=="HTTP 422: Try later","missing error falls back");
 check(httpFailureDetail(422,"{\"error\":\"First\",\"message\":\"Second\"}")=="HTTP 422: First","error takes precedence");
 check(httpFailureDetail(422,"{} ")=="HTTP 422","empty JSON");
 check(httpFailureDetail(422,"")=="HTTP 422","empty body");
 check(httpFailureDetail(422,"{bad")=="HTTP 422","malformed JSON");
 check(httpFailureDetail(422,"{\"error\":5,\"message\":\"Try later\"}")=="HTTP 422: Try later","non-string error fallback");
 std::string pl; for(int i=0;i<61;i++) pl+="ą"; auto truncated=httpFailureDetail(422,"{\"error\":\""+pl+"\"}"); check(truncated=="HTTP 422: "+pl.substr(0,120),"UTF8 exactly 120 bytes");
 std::string crossing(119,'a'); crossing+="ą"; auto d=httpFailureDetail(422,"{\"error\":\""+crossing+"\"}"); check(d=="HTTP 422: "+std::string(119,'a'),"UTF8 crossing boundary");
 std::string emoji(118,'a'); emoji+="😀"; check(httpFailureDetail(422,"{\"message\":\""+emoji+"\"}")=="HTTP 422: "+std::string(118,'a'),"four-byte UTF8 crossing boundary");
 std::string large(5000,'x'); check(httpFailureDetail(503,"{\"error\":\""+large+"\"}")=="HTTP 503: "+std::string(120,'x'),"large retained field truncated after parsing");
 check(httpStatusDetail(404)=="HTTP 404","file GET status only");
 CatalogActivity c; UiScreen screen; c.finishDownload(HttpDownloader::HTTP_ERROR,"HTTP 422: SYNTHETIC_PRIVATE_MARKER");
 check(c.state==CatalogActivity::State::ERROR && c.updated,"actual finish enters error state");
 check(c.buildStatusScreen(screen,false,false) && rendered.size()==2 && rendered[1]=="Download failed (HTTP 422: SYNTHETIC_PRIVATE_MARKER)","actual error screen receives detail");
 check(logline.find("SYNTHETIC_PRIVATE_MARKER")==std::string::npos,"server detail absent from serial log");
 CatalogActivity plain; plain.finishDownload(HttpDownloader::HTTP_ERROR); check(plain.errorMessage=="Download failed","no HTTP answer stays generic");
 CatalogActivity cancel; cancel.finishDownload(HttpDownloader::ABORTED); check(cancel.finished && cancel.state!=CatalogActivity::State::ERROR,"cancel remains non-error");
}
