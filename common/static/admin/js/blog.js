
// 博客分类局部刷新
$('#cat-0').css("background","#d9534f");
$('#cat-0').css("color","#FFF");

function BlogCat(obj, lid){
    $('.blog-cat').css("background","#FFF");
    let url = window.location.href;
    let href_url = url.replace("blog_list", "");
    let req_url = url +"?lid=" + lid;
    let html = '';
    $.ajax({
        url: req_url,
        data: {},
        type: "GET",
        dataType: "json",
        success: function (data) {
            if (data.code == 200){
                blog_list = JSON.parse(data.result.blog_list);
                for (let i = 0; i < blog_list.length; i++){
                   let hddatetime = formatDate(blog_list[i].fields.created_at);
                   html += `
                      <div class="article-box clearfix excerpt-1">
                        <h2>
                            <a href="${ href_url }blog_detail-${ blog_list[i].pk }.html" target="_blank" title="${ blog_list[i].fields.title }">
                                ${ blog_list[i].fields.title }
                            </a>
                        </h2>
    
                        <p class="txtcont hidden-xs">
                            <a href="${ href_url }blog_detail-${ blog_list[i].pk }.html"  target="_blank" title="${ blog_list[i].fields.title }">
                                ${ blog_list[i].fields.excerpt }
                            </a>
                        </p>
    
                        <div class="meta">
                            <span class="item" style="margin-right:10px">
                                <i class="fa fa-user"></i><span>${ blog_list[i].fields.account_name } </span>
                            </span>
                            <time class="item">
                                <i class="fa fa-clock-o"></i>${ hddatetime }
                            </time>
    
                            <span class="item blog-like" onclick="TopicLike(this, ${ blog_list[i].pk })">
                                <img src="static/images/dz.svg"><span id="goodNews-${ blog_list[i].pk }">${ blog_list[i].fields.like }</span>
                            </span>
    
                            <span class="item blog-commet">
                                <img src="static/images/msg.svg"><span>${ blog_list[i].fields.like }</span>
                            </span>
    
                            <span class="item blog-views">
                                <img src="static/images/kg.svg"><span>${ blog_list[i].fields.views }</span>
                            </span>
                        </div>
                      </div>
                   `;
                }
            }
            $('#blog-list').html(html);
        }
    });
    $('#cat-'+lid).css("background","#d9534f");
    $('#cat-'+lid).css("color","#FFF");
}


// 博客全部懒加载
let BlogDom = jQuery('#blog-list');
var pages = 2;
function BlogLoadMore(obj) {
    let url= window.location.href;
    let req_url = url+ "?page=" + pages;
    let href_url = url.replace("blog_list", "");
    let html = '';
    $.ajax({
        url: req_url,
        data: {},
        type: "GET",
        dataType: "json",
        success: function (response) {
            if (response.ok === true) {
                let retData = JSON.parse(response.result.blog_list);
                console.log(retData)
                if(retData.length > 1 ) {
                   for(let i  = 0; i < retData.length; i++) {
                        let hddatetime = formatDate(retData[i].fields.created_time);
                        html += `
                            <div class="article-box clearfix excerpt-1">
                                <h2>
                                    <a href="${ href_url }blog_detail-${ retData[i].pk }.html" target="_blank" title="${ retData[i].fields.title }">
                                        ${ retData[i].fields.title }
                                    </a>
                                </h2>
            
                                <p class="txtcont hidden-xs">
                                    <a href="${ href_url }blog_detail-${ retData[i].pk }.html"  target="_blank" title="${ retData[i].fields.title }">
                                        ${ retData[i].fields.excerpt }
                                    </a>
                                </p>
            
                                <div class="meta">
                                    <span class="item" style="margin-right:10px">
                                        <i class="fa fa-user"></i><span>${ retData[i].fields.account_name }</span>
                                    </span>
                                    <time class="item">
                                        <i class="fa fa-clock-o"></i>${ hddatetime }
                                    </time>
            
                                    <span class="item blog-like" onclick="BlogLike(this, ${ retData[i].pk })">
                                        <img src="static/images/dz.svg"><span id="goodBlog-{{ list.id }}">${ retData[i].fields.like }</span>
                                    </span>
            
                                    <span class="item blog-commet">
                                        <img src="static/images/msg.svg"><span>${ retData[i].fields.like }</span>
                                    </span>
            
                                    <span class="item blog-views">
                                        <img src="static/images/kg.svg"><span>${ retData[i].fields.views }</span>
                                    </span>
                                </div>
                            </div>
                        `;
                    }
                    BlogDom.append(html);
               } else {
                    var tphtml = '';
                    $('#blog-no-more-img').remove();
                    tphtml = `<p style="margin-top:8px">没有了，已经见低了</p>`;
                    $('#blog-no-more').html(tphtml);
               }
            }
        }
    });
    pages = pages + 1;
}


function AddBlogComment(obj, blog_id, reply_id, account_id) {
    var url = window.location.href;
    var index = url.lastIndexOf("\/");
    var url_str = url.substring(0, index + 1);
    var req_url = url_str + "blog_commet_reply";
    var blog_comments = $("#blog-comment").val();
    if (blog_comments == "" || blog_comments==null) {
        showMsg("评论内容不能为空");
        return ;
    }

    $.ajax({
        url: req_url,
        data: {
            "blog_id":blog_id,
            "reply_id":reply_id,
            "user_id":account_id,
            "content":blog_comments
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

function BlogLike(obj, id) {
    var url = window.location.href;
    var index = url.lastIndexOf("\/");
    var url_str = url.substring(0, index + 1);
    var temp_url = url_str + "blog_like";
    var req_url = temp_url +"?id=" + id;
    console.log(req_url)
    var goodIndex = id;
    $.ajax({
        url: req_url,
        data: {},
        type: "GET",
        dataType: "json",
        success: function (result) {
            $('#goodBlog-' + goodIndex ).text(result.total_like);
        }
    });
}

function BlogRelyLike(obj, id) {
    var url = window.location.href;
    var index = url.lastIndexOf("\/");
    var url_str = url.substring(0, index + 1);
    var temp_url = url_str + "blog_reply_like";
    var req_url = temp_url +"?id=" + id;
    var goodIndex = id;
    $.ajax({
        url: req_url,
        data: {},
        type: "GET",
        dataType: "json",
        success: function (result) {
            $('#goodBlogComment-' + goodIndex ).text(result.blog_reply_like);
        }
    });
}

function BlogCommentReply(obj, blog_id, reply_id, account_id) {
    $('#reply-li-js').remove();
    let CommentDom = jQuery('#comment-li-'+reply_id);
    var html = `
        <div class="topic-text" style="margin-top:20px; margin-left:50px" id="reply-li-js">
           <textarea id="blog-comment-reply" placeholder="请输入您想说的话" autofocus maxlength="280" rows="1" cols="90"></textarea>
           <input onclick="AddBlogReply(this, ${blog_id}, ${reply_id}, ${account_id})" style="padding:0 0; margin-bottom:16px; height:26px; width:50px" type="button" class="btn btn-primary" value="回复"/>
        </div>`;
    CommentDom.append(html);
}

function AddBlogReply(obj, blog_id, reply_id, account_id) {
     var url = window.location.href;
    var index = url.lastIndexOf("\/");
    var url_str = url.substring(0, index + 1);
    var req_url = url_str + "blog_commet_reply";
    var comments = $("#blog-comment-reply").val();
    if (comments == "" || comments==null) {
        showMsg("评论内容不能为空");
        return ;
    }
    $.ajax({
        url: req_url,
        data: {
            "blog_id":blog_id,
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
