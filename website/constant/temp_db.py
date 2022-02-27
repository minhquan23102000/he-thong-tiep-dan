paper = {
    'khai sinh': [{
        'title': 'giấy chứng nhận kết hôn',
        'src': '/static/img/chung_nhan_ket_hon.jpg'
    }, {
        'title': 'sổ thường trú',
        'src': '/static/img/cm_noi_o.jpg'
    }, {
        'title': 'giấy chứng sinh',
        'src': '/static/img/giay_chung_sinh.jpg'
    }, {
        'title': 'giấy tờ tùy thân',
        'src': '/static/img/giay_tuy_than.jpg'
    }, {
        'title': 'to_khai',
        'src': '/static/img/to_khai_khai_sinh.jpg'
    }],
    'đăng ký kết hôn': [{
        'title': 'giấy tờ tùy thân',
        'src': '/static/img/giay_tuy_than.jpg'
    }, {
        'title': 'to_khai',
        'src': '/static/img/to_khai_ket_hon.jpg'
    }, {
        'title':
        'giấy xác nhận tình trạng hôn nhân',
        'src':
        '/static/img/giay_xac_nhan_tinh_trang_hon_nhan.jpg'
    }],
    'khai sinh lại': [{
        'title': 'giấy tờ tùy thân',
        'src': '/static/img/giay_tuy_than.jpg'
    }, {
        'title': 'to_khai',
        'src': '/static/img/to_khai_khai_sinh_lai.jpg'
    }, {
        'title': 'sổ thường trú',
        'src': '/static/img/cm_noi_o.jpg'
    }, {
        'title': 'bản sao khai sinh',
        'src': '/static/img/trich_luc_khai_sinh.jpg'
    }],
    'Đăng ký thường trú': [{
        'title': 'giấy tờ tùy thân',
        'src': '/static/img/giay_tuy_than.jpg'
    }, {
        'title': 'sổ thường trú',
        'src': '/static/img/cm_noi_o.jpg'
    }, {
        'title': 'to_khai',
        'src': '/static/img/to_khai_thuong_tru.jpg'
    }]
}

thutuc = {
    'khai sinh': "Giấy khai sinh là giấy tờ hộ tịch gốc của cá nhân. Mọi hồ sơ, giấy tờ của cá nhân sau này đều phải cần theo thông tin của giấy khai sinh của người đó.",
    'khai sinh lại': "Giấy khai sinh là giấy tờ hộ tịch gốc của cá nhân. Mọi hồ sơ, giấy tờ của cá nhân sau này đều phải cần theo thông tin của giấy khai sinh của người đó.",
    'Đăng ký thường trú': "Là việc công dân đăng ký nơi ở thường trú của mình với cơ quan nhà nước có thẩm quyền và được cơ quan này làm thủ tục đăng ký thường trú, cấp sổ hộ khẩu cho họ.",
    'đăng ký kết hôn': "Đăng ký kết hôn là thủ tục do pháp luật quy định nhằm công nhận việc xác lập quan hệ hôn nhân giữa hai bên nam, nữ khi kết hôn."
}

paper_description = {
    'giấy tờ tùy thân': ["Giấy tờ tùy thân có hiệu lực bao gồm, giấy CMND, căn cước công dân hoặc bất kì loại giấy tờ có hiệu lực pháp lý xác minh bản thân người làm giấy.", '/static/img/giay_tuy_than.jpg'],
    'sổ thường trú':["Là giấy tờ xác mình nơi cư trú. Các giấy tờ có hiệu lực bao gồm: giấy chứng nhận nhân khẩu tập thể, sổ tạm trú, sổ thường trú, sổ hộ khẩu.", '/static/img/cm_noi_o.jpg'],
    'giấy chứng sinh': ["Giấy chứng sinh – một loại giấy tờ quan trọng xác nhận sự ra đời của một con người. Được bệnh viện, trạm y tế, cơ sở sinh ra bé cấp. Trường hợp không có giấy chứng sinh thì phải có văn bản xác nhận của người làm chứng về việc sinh. Trong trường hợp không có người làm chứng thì phải có giấy cam đoan về việc sinh.", '/static/img/giay_chung_sinh.jpg'],
    'giấy chứng nhận kết hôn': ["Giấy chứng nhận kết hôn là văn bản do cơ quan nhà nước có thẩm quyền cấp cho hai bên nam, nữ khi đăng ký kết hôn, nhằm xác lập mối quan hệ hôn nhân giữa hai người nam nữ.",  '/static/img/chung_nhan_ket_hon.jpg'],
    'giấy xác nhận tình trạng hôn nhân': ["Giấy xác nhận tình trạng hôn nhân được sử dụng để kết hôn tại cơ quan có thẩm quyền của Việt Nam, kết hôn tại cơ quan có thẩm quyền của nước ngoài ở nước ngoài hoặc sử dụng vào mục đích khác. Giấy xác nhận tình trạng hôn nhân không có giá trị khi sử dụng vào mục đích khác với mục đích ghi trong Giấy xác nhận.", '/static/img/giay_xac_nhan_tinh_trang_hon_nhan.jpg'],
    'bản sao khai sinh': ["Là bản sao giấy khai sinh. Bạn có thể nhận bản sao thông qua cơ quan đăng ký hộ tịch. Thông thường là Ủy ban nhân dân cấp xã (khi khai sinh không có yếu tố nước ngoài) hoặc Ủy ban nhân dân cấp huyện nơi bạn sinh ra (nếu khai sinh có yếu tố nước ngoài).", '/static/img/trich_luc_khai_sinh.jpg']
}


def make_img_guide(tag):
    data = dict()
    
    data['description'] = thutuc[tag]
    data['paper'] = []
    
    for di in paper[tag]:
        if not di['title'] == 'to_khai':
            di['description'] = paper_description[di['title']][0]
            data['paper'].append(di)
        else:
            data['to_khai'] = di
    return data
        
        
from chatbot.models import Paper, PaperLinkTag, Tag
from website import db


def get_thutuc(tag):
    return db.session.query(Tag).filter(Tag.name == tag).first()

def get_paper(paper):
    return db.session.query(Paper).filter(Paper.paper_name == paper).first()

def update_thutuc_description(mThutuc: Tag):
    mThutuc.description = thutuc[thutuc.name]
    return mThutuc

def insert_papers():
    for k, v in paper_description.items():
        paper = Paper(paper_name = k, img_src = v[1])
        db.session.add(paper)
        
    db.session.commit()
    db.session.flush()
    
def link_paper_tag(mThutuc: Tag, hoso: Paper):
    paperlink = PaperLinkTag(tag_id = mThutuc.id, paper_id = hoso.id, description = paper_description[hoso.paper_name][0])
    return paperlink

def insert_temp_db():
    global thutuc, paper, paper_description
    #insert_papers()    
    
    for tt_name, tt_description in thutuc.items():
        print(tt_name)
        tt = get_thutuc(tt_name)
        tt.description = tt_description
        
        #link paper 
        for mPaper in paper[tt.name]:
            if mPaper['title'] != 'to_khai':
                newPaper = get_paper(mPaper['title'])
                paperLink = link_paper_tag(tt, newPaper)
                db.session.add(paperLink)
                
        db.session.commit()
