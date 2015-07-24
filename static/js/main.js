$(function () {
//	var msg = new SpeechSynthesisUtterance('Hello World');
//    window.speechSynthesis.speak(msg);
//	speechSynthesis.getVoices().forEach(function(voice) {
//		console.log(voice.name, voice.default ? '(default)' :'', voice.lang);
//	});
	$('#editTable').tableScroll({
		scrollHeight: 250
	});
});

function say(text, lang) {
	var msg = new SpeechSynthesisUtterance(text);
	msg.lang = lang;
	window.speechSynthesis.speak(msg);
}
