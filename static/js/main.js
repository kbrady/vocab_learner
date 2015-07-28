$(function () {
	$('#editTable').tableScroll({
		scrollHeight: 250
	});
});

function get_lang() {
	return speechSynthesis.getVoices().map(function(voice) { return voice.lang }).filter(function(val,index,self) { return self.indexOf(val) === index });
}

function say(text, lang) {
	var msg = new SpeechSynthesisUtterance(text);
	msg.lang = lang;
	window.speechSynthesis.speak(msg);
}
