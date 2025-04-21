import os
import sys

import wikidot  # type: ignore
from wikidot.common import exceptions  # type: ignore

# このスクリプトが存在するディレクトリを取得
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 取得対象のページ情報 (サイトのUnix名, ページ名)
TARGET_PAGES = [
    ("scp-jp", "tag-list"),
    ("scp-jp", "fragment:tag-list-basic"),
    ("scp-jp", "fragment:tag-list-series"),
    ("scp-jp", "fragment:tag-list-universe"),
    ("scp-jp", "fragment:tag-list-event"),
    ("scp-jp", "fragment:tag-list-unused"),
    ("scp-jp", "fragment:tag-list-faq"),
    ("05command", "tech-hub-tag-list"),
]


def retrieve_and_save_page(
    client: wikidot.Client, site_unix_name: str, page_fullname: str
):
    """
    指定されたWikidotページのソースを取得し、ファイルに保存する関数
    """
    print(f"処理中: {site_unix_name}:{page_fullname} ...")
    try:
        # サイトオブジェクトを取得
        site = client.site.get(site_unix_name)
        if not site:
            print(
                f"  エラー: サイト '{site_unix_name}' が見つかりません。",
                file=sys.stderr,
            )
            return False

        # ページオブジェクトを取得
        page = site.page.get(
            page_fullname, raise_when_not_found=True
        )  # 見つからない場合は例外発生

        # ページソースを取得
        page_source = page.source.wiki_text  # type: ignore

        # 保存ファイル名を生成 (例: scp-jp_tag-list.txt)
        # フルネーム中の':'を'_'に置換するなど、ファイル名として安全な形式にする
        safe_page_name = page_fullname.replace(":", "_").replace("/", "_")
        output_filename = f"{safe_page_name}.txt"
        # サイト名のディレクトリを作成
        output_dir = os.path.join(SCRIPT_DIR, site_unix_name)
        os.makedirs(output_dir, exist_ok=True)
        output_filepath = os.path.join(output_dir, output_filename)

        # ファイルに保存 (UTF-8エンコーディング)
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write(page_source)

        # 相対パスで表示
        relative_path = os.path.relpath(output_filepath, SCRIPT_DIR)
        print(f"  成功: '{relative_path}' として保存しました。")
        return True

    except exceptions.NotFoundException as e:
        print(
            f"  エラー: ページ '{site_unix_name}:{page_fullname}' が見つかりません。 ({e})",
            file=sys.stderr,
        )
        return False
    except exceptions.ForbiddenException as e:
        print(
            f"  エラー: ページ '{site_unix_name}:{page_fullname}' へのアクセス権がありません。サイトがプライベートである可能性があります。 ({e})",
            file=sys.stderr,
        )
        return False
    except Exception as e:
        print(
            f"  予期せぬエラーが発生しました ({site_unix_name}:{page_fullname}): {e}",
            file=sys.stderr,
        )
        return False


def main():
    """
    メイン処理
    """
    print("Wikidotページ取得処理を開始します...")

    # Wikidotクライアントを初期化 (ログイン不要)
    client = wikidot.Client(logging_level="ERROR")  # INFOやDEBUGにすると詳細ログが出る

    success_count = 0
    error_count = 0

    # 各ページを処理
    for site_name, page_name in TARGET_PAGES:
        if retrieve_and_save_page(client, site_name, page_name):
            success_count += 1
        else:
            error_count += 1

    print("\n処理が完了しました。")
    print(f"成功: {success_count}件, 失敗: {error_count}件")


if __name__ == "__main__":
    main()
