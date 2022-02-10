
var pages = 2;
function VideoLoadMore(obj) {
    let url= window.location.href;
    let req_url = url+ "?page=" + pages;
    let href_url = url.replace("video_list", "");
    let html = '';
    $.ajax({
        url: req_url,
        data: {},
        type: "GET",
        dataType: "json",
        success: function (response) {
            if (response.ok === true) {
                let video_list = JSON.parse(response.result.video_list);
                if(video_list.length > 1 ) {
                   for(let i  = 0; i < video_list.length; i++) {
                        html += `
                            <div class="_20Cq3Rn7_0">
                                <div class="_2sej44xY_0">
                                    <a data-seo="" href="${ href_url }video_detail-${ video_list[i].pk }.html">
                                        <img src="${ href_url }media/${ video_list[i].fields.video_img }" alt="" class="_1miPDP4s_0">
                                    </a>
                                </div>
                                <div class="_3M3E-ESU_0">
                                    <div class="_3gQBs_6X_0">
                                        <div class="_3G50nw0p_0">
                                            <h2>${ video_list[i].fields.title }</h2>
                                            <p> 已有 ${ video_list[i].fields.views } 人学习</p>
                                        </div>
                                    </div>
                                    <div class="_14n6BJoa_0">
                                        <ul>
                                            <li>
                                                <a href="${ href_url }video_detail-${ video_list[i].pk }.html" class="_10vvBdC9_0">
                                                    <span class="_ffA7FdL_0">简介</span>
                                                    ${ video_list[i].fields.excerpt }
                                                </a>
                                            </li>
                                        </ul>
                                    </div>
                                    <div class="_2zRFFX7P_0">
                                        <p class="_14cxbu2p_0">
                                            <i class="fa fa-user"></i><span class="_1BSc9YvC_0" style="margin-left:10px; color:#1b6d85; font-size:14px">
                                            讲师: ${ video_list[i].fields.user } | 币信高级区块链研发工程师
                                        </span>
                                        </p>
                                        <div class="_1NLR_mQs_0">
                                            <button class="_272_Yrle_0">立即学习</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        `;
                    }
                    $("#video-list-load").append(html);
               } else {
                    var tphtml = '';
                    $('#video-no-more-img').remove();
                    tphtml = `<p style="margin-top:8px">没有了，已经见低了</p>`;
                    $('#video-no-more').html(tphtml);
               }
            }
        }
    });
    pages = pages + 1;

}


$('#cat-0').css("background","#d9534f");
$('#cat-0').css("color","#FFF");

function VideoCat(obj, lid){
    $('.v-tag').css("background","#FFF");
    $('.v-tag').css("color","#888");
    let url = window.location.href;
    let req_url = url +"?lid=" + lid;
    let href_url = url.replace("video_list", "");
    console.log(req_url);
    let html = '';
    $.ajax({
        url: req_url,
        data: {},
        type: "GET",
        dataType: "json",
        success: function (data) {
            if (data.code == 200){
                video_list = JSON.parse(data.result.video_list);
                for (let i = 0; i < video_list.length; i++){
                   let hddatetime = formatDate(video_list[i].fields.created_at);
                   html += `
                    <div class="_20Cq3Rn7_0">
                        <div class="_2sej44xY_0">
                            <a data-seo="" href="${ href_url }video_detail-${ video_list[i].pk }.html">
                                <img src="${href_url}media/${ video_list[i].fields.video_img }" alt="" class="_1miPDP4s_0">
                            </a>
                        </div>
                        <div class="_3M3E-ESU_0">
                            <div class="_3gQBs_6X_0">
                                <div class="_3G50nw0p_0">
                                    <h2>${ video_list[i].fields.title }</h2>
                                    <p> 已有 ${ video_list[i].fields.views } 人学习</p>
                                </div>
                            </div>
                            <div class="_14n6BJoa_0">
                                <ul>
                                    <li>
                                        <a href="${ href_url }video_detail-${ video_list[i].pk }.html" class="_10vvBdC9_0">
                                            <span class="_ffA7FdL_0">简介</span>
                                            ${ video_list[i].fields.excerpt }
                                        </a>
                                    </li>
                                </ul>
                            </div>
                            <div class="_2zRFFX7P_0">
                                <p class="_14cxbu2p_0">
                                    <i class="fa fa-user"></i><span class="_1BSc9YvC_0" style="margin-left:10px; color:#1b6d85; font-size:14px">
                                    讲师: ${ video_list[i].fields.user } | 币信高级区块链研发工程师
                                </span>
                                </p>
                                <div class="_1NLR_mQs_0">
                                    <button class="_272_Yrle_0">立即学习</button>
                                </div>
                            </div>
                        </div>
                    </div>
                   `;
                }
            }
            $('#video-list-load').html(html);
        }
    });
    $('#cat-'+lid).css("background","#d9534f");
    $('#cat-'+lid).css("color","#FFF");
}

function VideoTurn(obj, video_url) {
    var url = window.location.href;
    var index = url.lastIndexOf("\/");
    var url_str = url.substring(0, index + 1);
    var videoSrc = url_str + "media/" + video_url;
    console.log(videoSrc);
    document.getElementById("videoid").src=videoSrc ;
    document.getElementById("videoid").play();
}

function AddVideoComment(obj, video_id, reply_id, account_id) {
    var url = window.location.href;
    var index = url.lastIndexOf("\/");
    var url_str = url.substring(0, index + 1);
    var req_url = url_str + "set_video_commet";
    var video_comments = $("#video_comments").val();

    if (video_comments == "" || video_comments==null) {
        showMsg("评论内容不能为空");
        return ;
    }
    $.ajax({
        url: req_url,
        data: {
            "video_id":video_id,
            "reply_id":reply_id,
            "user_id":account_id,
            "content":video_comments
        },
        type: "POST",
        dataType: "json",
        success: function (result) {
            console.log(result);
            if (result.code == 200) {
                window.location.reload();
            } else if (result.code == 1000) {
                showMsg(result.msg);
            } else {
                showMsg("未知类型错误");
            }
        }
    });
}

function VideoLike(obj, id) {
    var url = window.location.href;
    var index = url.lastIndexOf("\/");
    var url_str = url.substring(0, index + 1);
    var temp_url = url_str + "video_like";
    var req_url = temp_url +"?id=" + id;
    var goodIndex = id;
    $.ajax({
        url: req_url,
        data: {},
        type: "GET",
        dataType: "json",
        success: function (result) {
            $('#goodVideo-' + goodIndex ).text(result.total_like);
        }
    });
}

function VideoRelyLike(obj, id) {
    var url = window.location.href;
    var index = url.lastIndexOf("\/");
    var url_str = url.substring(0, index + 1);
    var temp_url = url_str + "vedio_reply_like";
    var req_url = temp_url +"?id=" + id;
    var goodIndex = id;
    $.ajax({
        url: req_url,
        data: {},
        type: "GET",
        dataType: "json",
        success: function (result) {
            $('#goodVideoComment-' + goodIndex ).text(result.video_reply_like);
        }
    });

}

function VideoVideoReply(obj, video_id, reply_id, account_id) {
    $('#reply-li-video').remove();
    let VideoDom = jQuery('#video-comment-li-'+video_id);
    var html = `
        <div class="topic-text" style="margin-top:20px; margin-left:50px" id="reply-li-video">
           <textarea id="video-comment-reply" placeholder="请输入您想说的话" autofocus maxlength="280" rows="1" cols="90"></textarea>
           <input onclick="AddBVideoReply(this, ${video_id}, ${reply_id}, ${account_id})" style="padding:0 0; margin-bottom:16px; height:26px; width:50px" type="button" class="btn btn-primary" value="回复"/>
        </div>`;
    VideoDom.append(html);
}


function AddBVideoReply(obj, video_id, reply_id, account_id) {
     var url = window.location.href;
    var index = url.lastIndexOf("\/");
    var url_str = url.substring(0, index + 1);
    var req_url = url_str + "set_video_commet";
    var comments = $("#video-comment-reply").val();
    if (comments == "" || comments==null) {
        showMsg("评论内容不能为空");
        return ;
    }
    $.ajax({
        url: req_url,
        data: {
            "video_id":video_id,
            "reply_id":reply_id,
            "user_id":account_id,
            "content":comments
        },
        type: "POST",
        dataType: "json",
        success: function (result) {
            if (result.code == 200) {
                window.location.reload();
            } else if (result.code == 1000) {
                showMsg(result.msg);
            } else {
                showMsg("未知类型错误");
            }
        }
    });
}


function showMsg(text, heading, icon) {
    if(heading == undefined) {
        var heading = "提示";
    }
    $.toast({
        text: text,
        heading: heading,
        icon: icon,
        position: 'top-center',
        textAlign: 'left',
        loader: false,
        loaderBg: '#ffffff',
    });
}

