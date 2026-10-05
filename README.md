i# Friday – APK kurulumu

1. GitHub’da yeni bir private repo aç ve bu klasördeki TÜM dosyaları yükle (.github klasörü dahil).
2. Repo > Actions > "Build APK" > Run workflow. İşlem yaklaşık 5 dakika sürer.
3. İşlem bitince Actions çalışmasının altındaki Artifacts bölümünden `friday-apk` paketini indir.
4. İndirilen zip dosyasından `app-debug.apk` dosyasını çıkar.
5. APK dosyasını telefona aktar ve aç.
6. Android’de "Bilinmeyen kaynaklardan yükleme" iznini ver.
7. Uygulamanın sağ üst köşesindeki ⚙ ikonuna bas.
8. `console.anthropic.com` üzerinden aldığın API anahtarını gir.

Model ayarı:
- `www/index.html` içindeki `MODEL` sabitini değiştirerek farklı model seçebilirsin.

Not:
- Bu dosya, projeyi GitHub üzerinde APK üretmeye uygun şekilde hazırlar.
- Yapılandırma doğru yapılırsa GitHub Actions ile otomatik APK üretimi gerçekleşir.
