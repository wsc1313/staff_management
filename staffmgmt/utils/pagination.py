from django.utils.safestring import mark_safe
import copy
"""
分页组件类
"""

class Pagination(object):
    def __init__(self, req, queryset, page_param='page', page_size=10,):
        page = req.GET.get(page_param, '1')
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page_num = page
        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.page_queryset = queryset[self.start:self.end]

        query_dict = copy.deepcopy(req.GET)
        self.query_dict = query_dict
        self.page_param = page_param

        # 计算总页数
        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count



    def make_html(self):
        plus = 5
        if self.total_page_count <= plus * 2 + 1:
            start_page = 1
            end_page = self.total_page_count
        else:
            if self.page_num <= plus:
                start_page = 1
                end_page = plus * 2 + 1
            else:
                if self.page_num + plus > self.total_page_count:
                    end_page = self.total_page_count
                    start_page = self.total_page_count - plus * 2
                else:
                    start_page = self.page_num - plus
                    end_page = self.page_num + plus

        page_str_list = []
        self.query_dict.setlist(self.page_param, [1])
        # 首页
        page_str_list.append(f'<li><a href="?{self.query_dict.urlencode()}">首页</a></li>')
        # 上一页
        if self.page_num > 1:
            self.query_dict.setlist(self.page_param, [self.page_num - 1])
            tpl = f'<li><a href="?{self.query_dict.urlencode()}">上一页</a></li>'
        else:
            self.query_dict.setlist(self.page_param, [1])
            tpl = f'<li><a href="?{self.query_dict.urlencode()}">上一页</a></li>'
        page_str_list.append(tpl)
        # 中间正常翻页阶段
        for i in range(start_page, end_page + 1):
            if i == self.page_num:
                self.query_dict.setlist(self.page_param, [i])
                tpl = f'<li class="active"><a href="?{self.query_dict.urlencode()}">{i}</a></li>'
            else:
                self.query_dict.setlist(self.page_param, [i])
                tpl = f'<li><a href="?{self.query_dict.urlencode()}">{i}</a></li>'
            page_str_list.append(tpl)
        # 下一页
        if self.page_num < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page_num + 1])
            tpl = f'<li><a href="?{self.query_dict.urlencode()}">下一页</a></li>'
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            tpl = f'<li><a href="?{self.query_dict.urlencode()}">下一页</a></li>'
        page_str_list.append(tpl)

        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append(f'<li><a href="?{self.query_dict.urlencode()}">尾页</a></li>')

        # 指定页面搜索
        serch_string = """
                <li>
                    <form method="get" style='float:left;margin-left:-1px'>
                        <input type="text" name='page' style='position:relative;float:left;display:inline-block;width:80px;border-radius:0;' 
                        class="form-control" placeholder="页码">
                        <button class="btn btn-default" type="submit">Go!</button>
                    </form>
                </li>
                """
        page_str_list.append(serch_string)
        page_str = mark_safe(''.join(page_str_list))
        return  page_str




