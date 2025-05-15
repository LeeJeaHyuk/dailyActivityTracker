import os
from glob import glob
from pathlib import Path

class DiffMerger:
    def __init__(self, diff_dir, remove_duplicates=True):
        """
        diff_dir: diff 파일들이 모여 있는 폴더 경로
        remove_duplicates: 동일한 추가/삭제 줄은 병합할 때 제거할지 여부
        """
        self.diff_dir = diff_dir
        self.remove_duplicates = remove_duplicates

    def get_original_file_key(self, filename):
        """파일명에서 원본 파일 키 추출 (.HHMMSS 부분 제거)"""
        if '.' in filename and filename[-6:].isdigit():
            return filename.rsplit('.', 1)[0]
        return filename

    def parse_diff_content(self, diff_content):
        """diff 내용을 줄 단위로 파싱해서 추가/삭제 리스트 추출"""
        added = set()
        removed = set()
        for line in diff_content.splitlines():
            if line.startswith('+') and not line.startswith('+++'):
                added.add(line[1:].strip())
            elif line.startswith('-') and not line.startswith('---'):
                removed.add(line[1:].strip())
        return added, removed

    def should_regenerate_final(self, file_key, filenames):
        """final 파일을 재생성해야 하는지 확인"""
        final_path = os.path.join(self.diff_dir, f"{file_key}_final.diff")
        if not os.path.exists(final_path):
            return True

        # final 파일의 수정 시간 확인
        final_mtime = os.path.getmtime(final_path)
        
        # 원본 파일들의 수정 시간 확인
        for filename in filenames:
            file_path = os.path.join(self.diff_dir, filename)
            if os.path.getmtime(file_path) > final_mtime:
                return True
        
        return False

    def merge_diffs(self):
        """폴더 내 diff 파일들을 파일별로 병합하고 중복 제거"""
        # 디렉토리 내의 파일들만 찾기
        diff_files = [f for f in os.listdir(self.diff_dir) if os.path.isfile(os.path.join(self.diff_dir, f))]
        diff_files = sorted(diff_files)

        file_groups = {}
        for filename in diff_files:
            if filename.endswith("_final.diff"):
                continue  # 이미 병합된 파일은 스킵
            file_key = self.get_original_file_key(filename)
            file_groups.setdefault(file_key, []).append(filename)

        for file_key, filenames in file_groups.items():
            # final 파일이 이미 존재하고 업데이트가 필요없는 경우 스킵
            if not self.should_regenerate_final(file_key, filenames):
                print(f"[스킵] {file_key}_final.diff는 이미 최신 상태입니다.")
                continue

            all_added = set()
            all_removed = set()

            for filename in sorted(filenames):
                file_path = os.path.join(self.diff_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    diff_content = f.read()
                added, removed = self.parse_diff_content(diff_content)
                all_added.update(added)
                all_removed.update(removed)

            # 최종 결과 만들기
            merged_diff_lines = []

            if self.remove_duplicates:
                # 중복 제거해서 저장
                for line in sorted(all_added):
                    merged_diff_lines.append(f"+{line}")
                for line in sorted(all_removed):
                    merged_diff_lines.append(f"-{line}")
            else:
                # 중복 제거 없이 그냥 모두 이어붙이기
                for filename in sorted(filenames):
                    file_path = os.path.join(self.diff_dir, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        diff_content = f.read()
                    merged_diff_lines.append(diff_content)

            final_diff_text = "\n".join(merged_diff_lines)

            # 최종 파일 저장
            final_path = os.path.join(self.diff_dir, f"{file_key}_final.diff")
            with open(final_path, 'w', encoding='utf-8') as f:
                f.write(final_diff_text)

            print(f"[완료] {final_path} 저장 완료.")

    def run(self):
        """병합 실행"""
        if not os.path.isdir(self.diff_dir):
            print(f"[오류] 폴더가 존재하지 않습니다: {self.diff_dir}")
            return
        self.merge_diffs()


if __name__ == "__main__":
    target_folder = input("병합할 diff 폴더 경로를 입력하세요: ").strip()
    merger = DiffMerger(diff_dir=target_folder)
    merger.run()
