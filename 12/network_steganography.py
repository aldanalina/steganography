#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практикалық жұмыс 12: Компьютерлік желілерде стеганография әдістерін қолдану
DNS tunneling, HTTP headers, ICMP payload талдауы
"""

import socket
import struct
import base64
import hashlib
from collections import defaultdict

class NetworkSteganography:
    def __init__(self):
        self.dns_queries = []
        self.http_headers = []
        self.icmp_packets = []
    
    def analyze_dns_query(self, query_name):
        """DNS сұрауын талдау"""
        # Ұзын субдомендерді тексеру
        if len(query_name) > 50:
            return True, "Ұзын субдомен"
        
        # Base64-қа ұқсас таңбалар
        if any(c in query_name for c in '+/='):
            return True, "Base64-қа ұқсас таңбалар"
        
        # Энтропия
        entropy = self.calculate_entropy(query_name)
        if entropy > 4.5:
            return True, f"Жоғары энтропия ({entropy:.2f})"
        
        return False, "Қалыпты"
    
    def calculate_entropy(self, data):
        """Энтропияны есептеу"""
        if not data:
            return 0
        
        counts = defaultdict(int)
        for char in data:
            counts[char] += 1
        
        entropy = 0
        length = len(data)
        for count in counts.values():
            p = count / length
            entropy -= p * (p.bit_length() - 1) if p > 0 else 0
        
        return entropy
    
    def analyze_http_header(self, header_name, header_value):
        """HTTP header талдауы"""
        suspicious = False
        reasons = []
        
        # Ұзын мәндер
        if len(header_value) > 200:
            suspicious = True
            reasons.append("Ұзын мән")
        
        # Base64-қа ұқсас
        if len(header_value) > 40 and all(c.isalnum() or c in '+/=' for c in header_value):
            suspicious = True
            reasons.append("Base64-қа ұқсас")
        
        # Жоғары энтропия
        entropy = self.calculate_entropy(header_value)
        if entropy > 5.0:
            suspicious = True
            reasons.append(f"Жоғары энтропия ({entropy:.2f})")
        
        return suspicious, reasons
    
    def analyze_icmp_payload(self, payload):
        """ICMP payload талдауы"""
        if not payload:
            return False, "Payload жоқ"
        
        # Энтропия
        entropy = self.calculate_entropy(payload)
        
        if entropy > 6.5:
            return True, f"Жоғары энтропия ({entropy:.2f}) - кодталған дерек болуы мүмкін"
        
        return False, "Қалыпты"
    
    def detect_dns_tunneling(self, dns_log):
        """DNS tunneling анықтау"""
        print(f"\n{'='*60}")
        print("DNS Tunneling Анықтау")
        print(f"{'='*60}")
        
        suspicious_queries = []
        
        for query in dns_log:
            query_name = query.get('query', '')
            is_suspicious, reason = self.analyze_dns_query(query_name)
            
            if is_suspicious:
                suspicious_queries.append({
                    'query': query_name,
                    'reason': reason,
                    'timestamp': query.get('timestamp', '')
                })
        
        print(f"\nКүдікті сұраулар саны: {len(suspicious_queries)}")
        for sq in suspicious_queries[:10]:  # Алғашқы 10
            print(f"  - {sq['query'][:50]}... ({sq['reason']})")
        
        return suspicious_queries
    
    def detect_http_steganography(self, http_log):
        """HTTP стеганография анықтау"""
        print(f"\n{'='*60}")
        print("HTTP Стеганография Анықтау")
        print(f"{'='*60}")
        
        suspicious_headers = []
        
        for entry in http_log:
            headers = entry.get('headers', {})
            for name, value in headers.items():
                is_suspicious, reasons = self.analyze_http_header(name, value)
                
                if is_suspicious:
                    suspicious_headers.append({
                        'header': name,
                        'value': value[:100],
                        'reasons': reasons
                    })
        
        print(f"\nКүдікті header-лар саны: {len(suspicious_headers)}")
        for sh in suspicious_headers[:10]:
            print(f"  - {sh['header']}: {sh['value']}... ({', '.join(sh['reasons'])})")
        
        return suspicious_headers
    
    def create_detection_report(self, dns_results, http_results, output_path):
        """Анықтау есебін жасау"""
        print(f"\n{'='*60}")
        print("Анықтау Есебін Жасау")
        print(f"{'='*60}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("Желілік Стеганография Анықтау Есебі\n")
            f.write("=" * 60 + "\n\n")
            
            f.write("DNS Tunneling:\n")
            f.write(f"Күдікті сұраулар: {len(dns_results)}\n")
            for r in dns_results[:20]:
                f.write(f"  - {r['query']} ({r['reason']})\n")
            
            f.write("\nHTTP Стеганография:\n")
            f.write(f"Күдікті header-лар: {len(http_results)}\n")
            for r in http_results[:20]:
                f.write(f"  - {r['header']}: {r['value'][:50]}... ({', '.join(r['reasons'])})\n")
        
        print(f"✓ Есеп сақталды: {output_path}")


def main():
    analyzer = NetworkSteganography()
    
    print("=" * 60)
    print("Желілік Стеганография Талдауы")
    print("=" * 60)
    
    # Мысал: DNS сұрауларды талдау
    sample_dns_log = [
        {'query': 'normal.example.com', 'timestamp': '2024-01-01 10:00:00'},
        {'query': 'verylongsubdomainname1234567890abcdefghijklmnopqrstuvwxyz.example.com', 'timestamp': '2024-01-01 10:00:01'},
        {'query': 'dGVzdA==.example.com', 'timestamp': '2024-01-01 10:00:02'},
    ]
    
    dns_results = analyzer.detect_dns_tunneling(sample_dns_log)
    
    # Мысал: HTTP header-ларды талдау
    sample_http_log = [
        {'headers': {
            'User-Agent': 'Mozilla/5.0',
            'Cookie': 'dGVzdA==.verylongbase64encodedstring1234567890abcdefghijklmnopqrstuvwxyz'
        }}
    ]
    
    http_results = analyzer.detect_http_steganography(sample_http_log)
    
    analyzer.create_detection_report(dns_results, http_results, '12/detection_report.txt')
    
    print("\n" + "=" * 60)
    print("Тест аяқталды!")
    print("=" * 60)


if __name__ == "__main__":
    main()

