<h1 style="text-align: center;"><strong>Python Code (PSNR, SSIM, MSSIM)</strong></h1>
<p><strong>IQA(image quality assessment)</strong>方法可以分為兩類，</p>
<p>1) <strong>subjective methods&nbsp;</strong>: 基於人眼觀察的感知結果來做評估。</p>
<p>2) <strong>objective methods&nbsp;</strong>: 基於數學計算來判別影像品質。</p>
<p>主觀方法確實是比較貼近我們的需求，但現今沒有任何一套標準來衡量感知的準確度，並且主觀評估需要耗費更多的人力與金錢，此方法較不方便；反而客觀方法利用數學計算來評估影像品質是目前來說最廣泛的評估方式。Objective methods 最常使用的就是 PSNR 與 SSIM。</p>
<ul>
<li><strong>PSNR(Peak Signal-to-Noise Ratio)</strong></li>
</ul>
<p style="padding-left: 60px;">計算兩張影像的 MES (mean squared error)，轉到 dB domain，辨別影像品質好壞，數字越大影像品質越好，正常spnr值會介於20~40之間。</p>
<ul>
<li><strong>SSIM(Structural Similarity)</strong></li>
</ul>
<p style="padding-left: 60px;">計算兩張影像之間的結構相似度，比對畫面的明度(luminance)、對比(contrast)與結構(structure)。SSIM會輸出0~1之間的數值，數值越接近於1，表示兩張影像越相似。</p>
<ul>
<li><strong>MSSIM(Mean Structural Similarity)</strong></li>
</ul>
<p style="padding-left: 60px;">SSIM是計算整張影像的mean與standard deviation，而MSSIM是將影像切成多個window，計算local window的mean&amp;std，將會得到更可靠的結構相似度結果。</p>
<p>&nbsp;</p>
<p>&nbsp;詳細計算公式可參考 :&nbsp;<a href="https://arxiv.org/pdf/1902.06068.pdf">https://arxiv.org/pdf/1902.06068.pdf</a></p>
<p>&nbsp;</p>
