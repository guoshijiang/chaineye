// 时间处理函数
function formatTen(num) {
   return num > 9 ? (num + "") : ("0" + num);
}

// 时间处理函数
let formatDate = function (date) {
    var date = new Date(new Date(date).valueOf() - 28800000);
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var day = date.getDate();
    var hour = date.getHours();
    var minute = date.getMinutes();
    var second = date.getSeconds();
    return year + "年" + formatTen(month) + "月" + formatTen(day + 1)+ "日 " + formatTen((hour-8))+ ":" + formatTen(minute);
};

// 贴吧点赞
function TopicLike(obj, id) {
    var url = window.location.href;
    var temp_url = url.replace("topic_list", "topic_like");
    var req_url = temp_url +"?id=" + id;
    var goodIndex = id;
    $.ajax({
        url: req_url,
        data: {},
        type: "GET",
        dataType: "json",
        success: function (result) {
            $('#goodNews-' + goodIndex ).text(result.total_like);
        }
    });
}

function CommentLike(obj, id) {
    var url = window.location.href;
    var index = url.lastIndexOf("\/");
    var url_str = url.substring(0, index + 1);
    var req_url = url_str + "comment_like?id=" + id;
    var goodIndex = id;
    $.ajax({
        url: req_url,
        data: {},
        type: "GET",
        dataType: "json",
        success: function (result) {
            $('#goodComment-' + goodIndex ).text(result.topic_reply_like);
        }
    });
}

// 博客分类局部刷新
$('#cat-0').css("background","#d9534f");
$('#cat-0').css("color","#FFF");

// 贴吧分类局部刷新
function TopicCat(obj, lid){
    $('.blog-cat').css("background","#FFF");
    let url = window.location.href;
    let req_url = url +"?lid=" + lid;
    let href_url = url.replace("topic_list", "");
    let html = '';
    $.ajax({
        url: req_url,
        data: {},
        type: "GET",
        dataType: "json",
        success: function (data) {
            if (data.code == 200){
                topic_list = JSON.parse(data.result.topic_list);
                for (let i = 0; i < topic_list.length; i++){
                   let hddatetime = formatDate(topic_list[i].fields.created_at);
                   html += `
                   <div class="article-box clearfix excerpt-1 topic-box">
                        <div class="profile clearfix">
                           <div class="profile_pic">
                              <img src="static/images/default_avatar.png" class="img-circle profile_img" />
                           </div>
                           <div class="profile_info">
                              <span>${ topic_list[i].fields.account_name }</span>
                              <h2>${ hddatetime }</h2>
                           </div>
                        </div>
                      
                        <div class="txtcont">
                            <article class="article-txtcont">${ topic_list[i].fields.content  }</article>
                        </div>

                        <div class="topic-bottom">
                            <div class="topic-like" onclick="TopicLike(this, ${ topic_list[i].pk })">
                                <img src="static/images/dz.svg"><span id="goodNews-${ topic_list[i].pk }">${ topic_list[i].fields.like }</span>
                            </div>
    
                            <div class="topic-commet">
                                <a href="${ href_url }topic_detail-${ topic_list[i].pk }.html" target="_blank" title="${ topic_list[i].fields.title }">
                                    <img src="static/images/msg.svg"><span>评论</span>
                                </a>
                            </div>
    
                            <div class="topic-views">
                                <img src="static/images/fx.svg"><span>分享</span>
                            </div>
                        </div>
                   </div>
                   `;
                }
            }
            $('#topic-list').html(html);
        }
    });
    $('#cat-'+lid).css("background","#d9534f");
    $('#cat-'+lid).css("color","#FFF");
}


// 贴吧全部懒加载
let Dom = jQuery('#topic-list');
var pages = 2;
function TopicLoadMore(obj){
    let url= window.location.href;
    let req_url = url+ "?page=" + pages;
    let html = '';
    $.ajax({
        url: req_url,
        data: {},
        type: "GET",
        dataType: "json",
        success: function (response) {
            if (response.ok === true) {
                let retData = JSON.parse(response.result.topic_list);
                console.log(retData);
                if(retData.length > 1 ) {
                   for(let i  = 0; i < retData.length; i++) {
                        let hddatetime = formatDate(retData[i].fields.created_time);
                        html += `
                            <div class="article-box clearfix excerpt-1 topic-box">
                                <div class="profile clearfix">
                                   <div class="profile_pic">
                                      <img src="static/images/default_avatar.png" class="img-circle profile_img" />
                                   </div>
                                   <div class="profile_info">
                                      <span>${ retData[i].fields.account_name }</span>
                                      <h2>${ hddatetime }</h2>
                                   </div>
                                </div>
                              
                                <div class="txtcont">
                                    <article class="article-txtcont">${ retData[i].fields.content  }</article>
                                </div>
        
                                <div class="topic-bottom">
                                    <div class="topic-like" onclick="TopicLike(this, ${ retData[i].pk })">
                                        <img src="static/images/dz.svg"><span id="goodNews-${ retData[i].pk }">${ retData[i].fields.like }</span>
                                    </div>
            
                                    <div class="topic-commet">
                                        <img src="static/images/msg.svg"><span>评论</span>
                                    </div>
            
                                    <div class="topic-views">
                                        <img src="static/images/fx.svg"><span>分享</span>
                                    </div>
                                </div>
                            </div>
                        `;
                    }
                    Dom.append(html);
               } else {
                    var tphtml = '';
                    $('#no-more-img').remove();
                    tphtml = `<p style="margin-top:8px">没有了，已经见低了</p>`;
                    $('#no-more').html(tphtml);
               }
            }
        }
    });
    pages = pages + 1;
}


function CommentReply(obj, topic_id, reply_id, account_id) {
    $('#reply-li-js').remove();
    let CommentDom = jQuery('#comment-li-'+reply_id);
    var html = `
        <div class="topic-text" style="margin-top:20px; margin-left:50px" id="reply-li-js">
           <textarea id="comment-reply" placeholder="请输入您想说的话" autofocus maxlength="280" rows="1" cols="90"></textarea>
           <input onclick="AddReply(this, ${topic_id}, ${reply_id}, ${account_id})" style="padding:0 0; margin-bottom:16px; height:26px; width:50px" type="button" class="btn btn-primary" value="回复"/>
        </div>`;
    CommentDom.append(html);
}

// 添加回复
function AddReply(obj, topic_id, reply_id, account_id) {
    var url = window.location.href;
    var index = url.lastIndexOf("\/");
    var url_str = url.substring(0, index + 1);
    var req_url = url_str + "set_comment_reply";
    var comments = $("#comment-reply").val();
    if (comments == "" || comments==null) {
        showMsg("评论内容不能为空");
        return ;
    }
    $.ajax({
        url: req_url,
        data: {
            "topic_id":topic_id,
            "reply_id":reply_id,
            "account_id":account_id,
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

// 添加评论
function AddComment(obj, topic_id, reply_id, account_id) {
    var url = window.location.href;
    var index = url.lastIndexOf("\/");
    var url_str = url.substring(0, index + 1);
    var req_url = url_str + "set_comment_reply";
    var comments = $("#comment").val();
    if (comments == "" || comments==null) {
        showMsg("评论内容不能为空");
        return ;
    }
    $.ajax({
        url: req_url,
        data: {
            "topic_id":topic_id,
            "reply_id":reply_id,
            "account_id":account_id,
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

