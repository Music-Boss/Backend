/*var vid = "3r_Z5AYJJd4",
    audio_streams = {},
    audio_tag = document.getElementById('youtube');

//fetch("https://"+vid+"-focus-opensocial.googleusercontent.com/gadgets/proxy?container=none&url=https%3A%2F%2Fwww.youtube.com%2Fget_video_info%3Fvideo_id%3D" + vid).then(response => {
fetch('https://thingproxy.freeboard.io/fetch/' + "https://www.youtube.com/get_video_info?video_id=" + vid).then(response => {
    if (response.ok) {
        response.text().then(data => {

            var data = parse_str(data),
                streams = (data.url_encoded_fmt_stream_map + ',' + data.adaptive_fmts).split(',');

            streams.forEach(function(s, n) {
                var stream = parse_str(s),
                    itag = stream.itag * 1,
                    quality = false;
                console.log(stream);
                switch (itag) {
                    case 139:
                        quality = "48kbps";
                        break;
                    case 140:
                        quality = "128kbps";
                        break;
                    case 141:
                        quality = "256kbps";
                        break;
                }
                if (quality) audio_streams[quality] = stream.url;
            });

            console.log(audio_streams);

            audio_tag.src = audio_streams['128kbps'];
            audio_tag.play();
        })
    } else{
        console.log(response);
    }
});

function parse_str(str) {
    return str.split('&').reduce(function(params, param) {
        var paramSplit = param.split('=').map(function(value) {
            return decodeURIComponent(value.replace('+', ' '));
        });
        params[paramSplit[0]] = paramSplit[1];
        return params;
    }, {});
}*/