#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日币圈新闻报告生成器
生成日期：2026年3月2日
"""

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

def set_chinese_font(run, font_name='Microsoft YaHei', size=11, bold=False):
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
    run.font.size = Pt(size)
    run.font.bold = bold

def add_heading_zh(doc, text, level=1):
    heading = doc.add_heading(level=level)
    run = heading.add_run(text)
    size = {1: 18, 2: 14, 3: 12}.get(level, 11)
    set_chinese_font(run, 'Microsoft YaHei', size, bold=True)
    heading.alignment = WD_ALIGN_PARAGRAPH.LEFT
    return heading

def create_crypto_report():
    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Microsoft YaHei'
    style._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    
    # 标题
    title = doc.add_heading(level=0)
    title_run = title.add_run('每日币圈新闻报告')
    set_chinese_font(title_run, 'Microsoft YaHei', 22, bold=True)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # 日期
    date_p = doc.add_paragraph()
    date_run = date_p.add_run('2026年3月2日')
    set_chinese_font(date_run, 'Microsoft YaHei', 12, bold=False)
    date_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph()
    
    # 市场概览
    add_heading_zh(doc, '一、市场概览', level=1)
    overview = """今日加密货币市场整体呈现谨慎观望态势。比特币持续面临7万美元关口压制，连续五个月的下跌趋势可能在3月延续。然而，期权市场显示交易员押注反弹至9万美元，市场正初现筑底信号。宏观层面，美以与伊朗的冲突升级导致地缘政治风险加剧，可能对风险资产造成短期冲击。监管方面，美国《Clarity法案》和稳定币监管框架的推进成为市场关注焦点。机构资金持续流入，比特币现货ETF本周净流入7.87亿美元，大型机构持续增持BTC。"""
    p = doc.add_paragraph()
    set_chinese_font(p.add_run(overview), 'Microsoft YaHei', 11, False)
    doc.add_paragraph()
    
    # 监管政策
    add_heading_zh(doc, '二、监管政策动态', level=1)
    reg_items = [
        ("白宫设定《Clarity法案》推进最后期限", "白宫设定3月1日为解决稳定币奖励争议和推进《Clarity法案》的最后期限，该法案的表决将成为3月加密市场关键事件之一。"),
        ("美国OCC就GENIUS法案征求意见", "美国货币监理署（OCC）就GENIUS法案支付型稳定币监管框架征求意见，稳定币监管框架的明确将有利于行业合规发展。"),
        ("韩国拟对加密影响者实行强制资产披露", "韩国议员提议对加密领域的影响者实行强制资产披露制度，加强市场透明度和投资者保护。"),
        ("美国利用技术优势大规模没收全球虚拟货币资产", "国家计算机病毒应急处理中心报告指出，美国利用技术与司法优势大规模没收全球虚拟货币资产，引发对数字资产主权安全的关注。"),
        ("明尼苏达州拟全面禁止加密货币ATM", "明尼苏达州拟全面禁止加密货币ATM，反映美国各州对加密资产监管态度的分化。")
    ]
    for i, (title, content) in enumerate(reg_items, 1):
        p = doc.add_paragraph()
        set_chinese_font(p.add_run(f"{i}. {title}"), 'Microsoft YaHei', 11, True)
        set_chinese_font(p.add_run(f" — {content}"), 'Microsoft YaHei', 11, False)
    doc.add_paragraph()
    
    # 机构动态
    add_heading_zh(doc, '三、机构动态', level=1)
    inst_items = [
        ("OpenAI获1100亿美元巨额融资", "OpenAI宣布以7300亿美元估值获得1100亿美元新投资，软银、英伟达各投300亿美元，亚马逊投500亿美元。科技巨头持续布局AI与加密交叉领域。"),
        ("Tether二级市场估值或达3750亿美元", "Tether二级市场估值可能高达3750亿美元，稳定币龙头地位进一步巩固。"),
        ("Circle股价大涨，USDC流通量创新高", "Circle股价大涨逾35%，Q4期末USDC流通量达753亿美元，稳定币市场竞争格局持续演变。"),
        ("花旗银行拟推出机构级比特币托管服务", "花旗银行拟于2026年晚些时候推出机构级比特币托管服务，传统金融巨头加速布局加密资产托管业务。"),
        ("摩根士丹利申请信托银行牌照布局加密业务", "摩根士丹利申请美国全国性信托银行牌照，布局加密托管与质押业务，华尔街大行持续进军加密领域。"),
        ("Block Q4增持340枚比特币", "Block披露其Q4增持340枚比特币，价值2200万美元，上市公司持续将BTC纳入资产配置。")
    ]
    for i, (title, content) in enumerate(inst_items, 1):
        p = doc.add_paragraph()
        set_chinese_font(p.add_run(f"{i}. {title}"), 'Microsoft YaHei', 11, True)
        set_chinese_font(p.add_run(f" — {content}"), 'Microsoft YaHei', 11, False)
    doc.add_paragraph()
    
    # 交易所动态
    add_heading_zh(doc, '四、交易所动态', level=1)
    exch_items = [
        ("Upbit将于3月30日下架DENT", "韩国主流交易所Upbit宣布将于3月30日下架DENT代币，投资者需注意持仓风险。"),
        ("币安钱包推出Sentio相关活动", "币安钱包推出Sentio（ST）相关Booster活动和Pre-TGE活动，持续布局新代币生态。"),
        ("Uniswap启动多链手续费分成投票", "Uniswap启动多链手续费分成投票，治理机制的完善将提升协议价值和代币持有者权益。")
    ]
    for i, (title, content) in enumerate(exch_items, 1):
        p = doc.add_paragraph()
        set_chinese_font(p.add_run(f"{i}. {title}"), 'Microsoft YaHei', 11, True)
        set_chinese_font(p.add_run(f" — {content}"), 'Microsoft YaHei', 11, False)
    doc.add_paragraph()
    
    # 链上数据
    add_heading_zh(doc, '五、链上数据监测', level=1)
    chain_items = [
        ("比特币现货ETF本周净流入7.87亿美元", "机构资金持续流入比特币现货ETF，显示长期投资者信心依然强劲。"),
        ("巨鲸地址过去30天增持15.2万枚BTC", "持有超1000枚BTC的地址过去30天内共增持约15.2万枚BTC，大户持续吸筹。"),
        ("贝莱德过去3天提取约7.17亿美元BTC", "贝莱德9小时前从Coinbase提现4082枚BTC，过去3天共提取约7.17亿美元BTC，机构资金动向值得关注。"),
        ("疑似Arrington Capital提取2万枚ETH", "疑似Arrington Capital钱包从币安和Deberit提取2万枚ETH，机构大额资金异动需密切关注。"),
        ("贝莱德向Coinbase存入1134枚BTC", "贝莱德向Coinbase存入1134枚BTC，约合7418万美元，机构资金进出频繁。")
    ]
    for i, (title, content) in enumerate(chain_items, 1):
        p = doc.add_paragraph()
        set_chinese_font(p.add_run(f"{i}. {title}"), 'Microsoft YaHei', 11, True)
        set_chinese_font(p.add_run(f" — {content}"), 'Microsoft YaHei', 11, False)
    doc.add_paragraph()
    
    # 市场分析
    add_heading_zh(doc, '六、市场分析观点', level=1)
    analysis_items = [
        ("比特币面临7万美元关口压制", "比特币面临7万美元关口压制，五个月连跌走势或难在3月终结，短期内价格压力依然存在。"),
        ("期权交易员押注反弹至9万美元", "比特币期权交易员押注价格反弹至9万美元，市场正初现筑底信号，多空分歧明显。"),
        ("Bitfinex报告：5.3万美元或为关键支撑", "Bitfinex报告指出，ETF流出与大户抛售令比特币承压，5.3万美元或为关键支撑位。"),
        ("比特币矿工投降期接近尾声", "分析指出比特币矿工投降期接近尾声，或预示比特币价格见底，历史规律值得关注。"),
        ("3月加密市场关键事件", "3月需关注：FOMC利率决议、《Clarity法案》表决、香港首批稳定币牌照、SUI/HYPE大额解锁等重大事件。")
    ]
    for i, (title, content) in enumerate(analysis_items, 1):
        p = doc.add_paragraph()
        set_chinese_font(p.add_run(f"{i}. {title}"), 'Microsoft YaHei', 11, True)
        set_chinese_font(p.add_run(f" — {content}"), 'Microsoft YaHei', 11, False)
    doc.add_paragraph()
    
    # 宏观/地缘政治
    add_heading_zh(doc, '七、宏观与地缘政治', level=1)
    macro_items = [
        ("美以对伊朗发动军事打击", "美以已对伊朗发动军事打击，伊朗最高领袖哈梅内伊遇害，中东地缘政治风险急剧升级。"),
        ("伊朗总统表示将复仇", "伊朗总统表示复仇是合法权利和义务，地区冲突可能进一步升级，需关注对全球风险资产的影响。"),
        ("伊朗股市暂停交易", "伊朗股市暂停交易至下周，市场避险情绪升温，黄金、原油等大宗商品可能受到提振。")
    ]
    for i, (title, content) in enumerate(macro_items, 1):
        p = doc.add_paragraph()
        set_chinese_font(p.add_run(f"{i}. {title}"), 'Microsoft YaHei', 11, True)
        set_chinese_font(p.add_run(f" — {content}"), 'Microsoft YaHei', 11, False)
    doc.add_paragraph()
    
    # 免责声明
    add_heading_zh(doc, '免责声明', level=1)
    disclaimer = """本报告仅供参考，不构成任何投资建议。加密货币市场波动剧烈，投资有风险，入市需谨慎。请投资者根据自身情况独立做出投资决策。"""
    p = doc.add_paragraph()
    set_chinese_font(p.add_run(disclaimer), 'Microsoft YaHei', 10, False)
    
    # 保存文档
    output_path = '/root/.openclaw/workspace/crypto_report_20260302.docx'
    doc.save(output_path)
    print(f"报告已生成：{output_path}")

if __name__ == '__main__':
    create_crypto_report()
