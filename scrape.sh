#!/bin/bash
# Scrape a competitor's active ads from the Meta Ad Library.
# usage: scrape.sh <page_id_or_library_url> <out_dir> [max_ads=20] [country=ALL]
# Output: <out_dir>/ads.tsv (one row per ad) + downloaded media in <out_dir>/media/
# Columns: library_id, start_date, versions, media_type, media_url, text
# Requires: npx agent-browser (npm i -g agent-browser or npx works), curl

set -u
INPUT="$1"; OUT="$2"; MAX="${3:-20}"; COUNTRY="${4:-ALL}"
mkdir -p "$OUT/media"

# Accept a raw page id or a full Ad Library URL containing view_all_page_id=
if [[ "$INPUT" =~ view_all_page_id=([0-9]+) ]]; then PID="${BASH_REMATCH[1]}"; else PID="$INPUT"; fi
URL="https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=$COUNTRY&is_targeted_country=false&media_type=all&search_type=page&sort_data[direction]=desc&sort_data[mode]=total_impressions&view_all_page_id=$PID"

npx agent-browser open "$URL" >/dev/null 2>&1
npx agent-browser wait 6000 >/dev/null 2>&1
for k in 1 2 3 4; do npx agent-browser scroll down 3000 >/dev/null 2>&1; npx agent-browser wait 2500 >/dev/null 2>&1; done

# Pull every ad card: walk up from the "Library ID" text node to the card container.
npx agent-browser eval "(()=>{
  const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);const hits=[];let n;
  while(n=w.nextNode()){if(/^Library ID/.test(n.textContent.trim()))hits.push(n.parentElement);}
  const seen=new Set();const out=[];
  hits.forEach(e=>{let el=e;for(let k=0;k<7;k++){el=el.parentElement;}if(!el)return;
    const txt=el.innerText.replace(/\\t/g,' ').replace(/\\n+/g,' | ');
    const id=(txt.match(/Library ID: (\\d+)/)||[])[1];if(!id||seen.has(id))return;seen.add(id);
    const start=(txt.match(/Started running on ([A-Za-z]{3} \\d{1,2}, \\d{4})/)||[])[1]||'';
    const ver=(txt.match(/(\\d+) ads use this creative/)||[])[1]||'1';
    const v=el.querySelector('video');
    let type='image',src='';
    if(v){type='video';src=v.src||v.currentSrc||'';}
    else{const im=[...el.querySelectorAll('img')].filter(i=>i.naturalWidth>250);if(im.length)src=im[0].src;}
    out.push([id,start,ver,type,src,txt.slice(0,3000)].join('\\t'));
  });
  return out.join('\\n');
})()" 2>/dev/null | sed 's/^"//;s/"$//; s/\\n/\n/g; s/\\t/\t/g; s/\\"/"/g' > "$OUT/ads.tsv"

N=$(grep -c . "$OUT/ads.tsv")
i=0
while IFS=$'\t' read -r id start ver type src txt; do
  [ $i -ge "$MAX" ] && break
  [ -z "$src" ] && continue
  ext="jpg"; [ "$type" = "video" ] && ext="mp4"
  f="$OUT/media/$id.$ext"
  [ -f "$f" ] || curl -sL "$src" -o "$f"
  i=$((i+1))
done < "$OUT/ads.tsv"
echo "page $PID: $N ads found, $i media files in $OUT/media"
