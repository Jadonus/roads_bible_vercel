var request = new Request("http://192.168.200.182:9000")
var result = await request.loadJSON()
console.log(result.responses)
let w = new ListWidget();
let res=result.
  responses.toString()
  
let text = w.addText(res);

Script.setWidget(w);
Script.complete();

w.presentLarge();
