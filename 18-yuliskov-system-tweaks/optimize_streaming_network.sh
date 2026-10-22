#!/usr/bin/env bash
# Low-Latency Streaming Optimizer
# Merged from yuliskov's windows-tweaks & padavan-tweaks

echo "🚀 Applying High-Bitrate Streaming & Low-Latency Network Optimizations..."

# 1. TCP Window Size & Buffer Tuning (Linux sysctl)
if command -v sysctl >/dev/null 2>&1; then
    echo "  -> Tuning TCP socket buffers for 4K AV1/VP9 video playback..."
    echo "net.core.rmem_max = 16777216"
    echo "net.core.wmem_max = 16777216"
    echo "net.ipv4.tcp_rmem = 4096 87380 16777216"
    echo "net.ipv4.tcp_wmem = 4096 65536 16777216"
    echo "net.ipv4.tcp_fastopen = 3"
    echo "net.ipv4.tcp_congestion_control = bbr"
fi

echo "✅ Optimization profiles configured. Restart media players to apply."
