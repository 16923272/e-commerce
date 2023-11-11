def baca_database(nama_file):
    try:
        with open(nama_file, 'r') as file:
            baris_data = file.readlines()
        return [data_per_baris.strip().split(';') for data_per_baris in baris_data]
    except FileNotFoundError:
        return [] # return list kosong kalau tidak ada data di db atau tidak ada db
    

def tulis_data_database(nama_file, email, password):
    with open(nama_file, 'a') as file:
        file.write(f"{email};{password}\n")


def login(email, password, database):
    # baca_database(database)
    for data in database:
        if data[0] != email:
            print(f"\nError | {nama_ecommerce}")
            print("Email tidak terdaftar. Harap menggunakan email terdaftar.")
            return
        elif data[0] == email:
            for data in database:
                if data[0] == email and data[1] == password:
                    return True
                print(f"\nError | {nama_ecommerce}")
                print("Password salah. Harap memasukkan password yang sesuai.")
            return False


def register(database):
    email_input = input("Email\t: ")
    password_input = input("Password: ")

    reenter_password = input("Re-enter Password: ")
    if password_input != reenter_password:
        print(f"\nError | {nama_ecommerce}")
        print("Password tidak sesuai. Harap ulangi pendaftaran.\n")
        
    elif password_input == reenter_password:
        # register kalau password sesuai
        for data in database:
            if data[0] == email_input:
                print(f"\nError | {nama_ecommerce}")
                print("Email sudah terdaftar. Harap menggunakan email lain.")
                return
        
        database.append([email_input, password_input])
        with open(db_user_account, 'a') as file:
            file.write(f"{email_input};{password_input}\n")

        print(f"\nRegister | {nama_ecommerce}")
        print(f"Pendaftaran berhasil. Silahkan lakukan login untuk mengakses {nama_ecommerce}.\n")


def display_cart(cart):
    for item in cart:
        product_code, product_name, price, quantity, total = item
        print(f"{product_code}. {product_name} - Rp {price} ({quantity} buah). Total: Rp {total}")


def display_products(products):
    for product in products:
        kode, nama, harga, jumlah_stok = product
        print(f"{kode}. {nama} - Rp {harga} ({jumlah_stok})")


def write_to_cart(filename, product):
    product_code = product[0]
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        found = False
        for i, line in enumerate(lines):
            cart_product_code = line.strip().split(';')[0]
            if cart_product_code == product_code:
                # update stok satu per satu
                stok = int(line.strip().split(';')[3]) + 1
                total = int(line.strip().split(';')[4]) + int(product[2])  # update total harga
                lines[i] = f"{product_code};{product[1]};{product[2]};{stok};{total}\n"
                found = True
                break

        if not found:
            # tambah produk kalau belum ada produk sejenis di keranjang
            stok = 1
            total = int(product[2])  # Calculate the total price
            lines.append(f"{product_code};{product[1]};{product[2]};{stok};{total}\n")

        # urutkan produk yang dibeli di dalam keranjang
        sorted_lines = sorted(lines, key=lambda x: x.strip().split(';')[0])

        with open(filename, 'w') as file:
            file.writelines(sorted_lines)
    except FileNotFoundError:
        # buat file keranjang kalau belum ada
        with open(filename, 'w') as file:
            stok = 1
            total = int(product[2])  # hitung total belanja seluruh produk
            file.write(f"{product_code};{product[1]};{product[2]};{stok};{total}\n")


def write_products(filename, products):
    with open(filename, 'w') as file:
        for product in products:
            file.write(';'.join(product) + '\n')


def order_product(products, kode, db_keranjang, db_produk):
    for product in products:
        if product[0] == kode:
            if int(product[3]) > 0:  # periksa apakah stok masih ada
                product[3] = str(int(product[3]) - 1)  # update stok yang tersisa
                print(f"\nPesan Produk Berhasil | {nama_ecommerce}")
                print(f"+1 Pesanan {product[1]} - Rp {product[2]} ditambahkan")

                # tambahkan produk yang dipesan ke dalam keranjang
                write_to_cart(db_keranjang, product)

                # update stok di db_produk
                write_products(db_produk, products)
                return True
            else:
                print(f"\nError | {nama_ecommerce}")
                print(f"Maaf, stok {product[1]} sudah habis.")
                return False
            
    print(f"\nError | {nama_ecommerce}")
    print("Kode produk salah. Mohon menyertakan kode yang sesuai.")
    return False


def checkout(cart):
    total_sum = sum(int(item[4]) for item in cart)
    print(f"\nTotal Sum: Rp {total_sum}")

    konfirmasi_checkout = input("Apakah anda ingin melakukan checkout? (ya/tidak): ").lower()
    if konfirmasi_checkout == 'ya':
        print("Memproses pembayaran...\n")

        konfirmasi_bayar = input("Apakah anda ingin melakukan konfirmasi pembayaran? (ya/tidak): ").lower()
        if konfirmasi_bayar == 'ya':
            print("\nMohon lengkapi data berikut.")
            nama_pembeli = input("Nama: ")
            alamat_pembeli = input("Alamat: ")
            rek_pembeli = input("Metode Pembayaran(PayIt!/COD): ")
            pengiriman = input("Pilih Metode Pengiriman(JNA/SiKilat/Whoosh): ")

            # generate kode random sebagai resi (Resi Pembayaran)
            kode_random = ''.join(random.choices(string.ascii_uppercase, k=3)) + ''.join(random.choices(string.digits, k=15))

            # buat file resi
            nama_resi = f"database/Resi/Resi_{nama_pembeli}_{kode_random}.txt"
            with open(nama_resi, 'w') as file_resi:
                file_resi.write("-----------------------------------------------------------\n")
                file_resi.write(f"Nomor Resi: {kode_random}\n")
                file_resi.write(f"Tanggal Pembelian: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n\n")
                file_resi.write(f"Nama: {nama_pembeli}\n")
                file_resi.write(f"Alamat: {alamat_pembeli}\n\n")
                file_resi.write("Rincian\n")

                for item in cart:
                    product_code, product_name, price, quantity, total = item
                    file_resi.write(f"{product_code}. {product_name} - Rp {price} ({quantity} buah). Total: Rp {total}\n")

                file_resi.write(f"\nTotal belanja: Rp {total_sum}\n")
                file_resi.write(f"Terima kasih telah berbelanja di {nama_ecommerce}\n")
                file_resi.write("-----------------------------------------------------------\n")

            print(f"\nPembayaran berhasil!\nResi pembayaran: {kode_random}")

            # kosongkan keranjang yang sudah dicheckout
            with open(db_keranjang, 'w') as cart_file:
                cart_file.write("")

            # konfirmasi belanja lagi atau tidak
            reorder = input("\nApakah anda ingin berbelanja kembali? (ya/tidak) ").lower()
            if reorder == 'ya':
                return True
            else:
                return False
        else:
            print("Pembayaran dibatalkan.")
    else:
        print("Checkout dibatalkan.")
    
    return False

def main():
    database = baca_database(db_user_account)

    if not database:
        print(f"\nError | {nama_ecommerce}")
        print("Tidak ada akun terdaftar. Harap register terlebih dahulu.")
        register(database)

    while True:
        print(f"Selamat datang di {nama_ecommerce}")
        print("1. Login")
        print("2. Register")
        print("0. Keluar")
        otentikasi = input("Silahkan login/register/keluar? [1/2/0]: ")

        # Login utama
        if otentikasi == '1':
            while True:
                print(f"\nLogin | {nama_ecommerce}")

                ot_email = input("Email\t: ")
                ot_password = input("Password: ")

                if login(ot_email, ot_password, database):
                    print(f"\nLogin | {nama_ecommerce}")
                    print(f"Login berhasil! Selamat berbelaja di {nama_ecommerce}")
                    while True:
                        print(f"\nHalaman Berbelanja | {nama_ecommerce}")
                        print("1. Cari Barang")
                        print("2. Periksa Keranjang")
                        print("0. Exit")
                        hal_belanja = input("Silahkan pilih fitur [1/2/0]: ")
                        
                        # bagian cari/beli produk
                        if hal_belanja == '1':
                            produk = baca_database(nama_file=db_produk)

                            if not produk:
                                print(f"\nError | {nama_ecommerce}")
                                print(f"Mohon maaf. Stok {nama_ecommerce} sedang kosong")
                                break
                            
                            print(f"\nCari Barang | {nama_ecommerce}")
                            display_products(produk)

                            while True:
                                kode_input = input("Masukkan kode produk untuk memesan (atau 'selesai' untuk kembali): ")

                                if kode_input.lower() == 'selesai':
                                    print(f"\nCari Barang | {nama_ecommerce}")
                                    print("Terima kasih sudah berbelanja. Silahkan periksa keranjang untuk checkout.")
                                    break

                                order_product(produk, kode_input, db_keranjang, db_produk)
                                print(f"\nCari Barang | {nama_ecommerce}")
                                display_products(produk)

                        # bagian cek keranjang dan checkout
                        elif hal_belanja == '2':
                            keranjang = baca_database(nama_file=db_keranjang)
                            print(f"\nPeriksa Keranjang | {nama_ecommerce}")
                            if not keranjang:
                                print(f"Saat ini keranjang anda kosong. Silahkan berbelanja terlebih dahulu.")
                            else:
                                display_cart(keranjang)
                                checkout(keranjang)

                        # keluar jika tidak belanja
                        elif hal_belanja == '0':
                            print(f"\nExit | {nama_ecommerce}")
                            print("Terima kasih. Selamat berbelanja kembali.")
                            break # keluar hal_belanja
                        
                        # salah input
                        else:
                            print(f"\nError | {nama_ecommerce}")
                            print("Maaf, fitur tersebut tidak tersedia.")
                    break # keluar setelah login
            break # keluar setelah otentikasi pertama


        # register di halaman utama
        elif otentikasi == '2':
            print(f"\nRegister | {nama_ecommerce}")
            register(database)


        # exit dari menu utama
        elif otentikasi == '0':
            print(f"\nExit | {nama_ecommerce}")
            print("Terima kasih. Selamat berbelanja kembali.")
            break


        # input salah di menu utama
        else:
            print(f"\nError | {nama_ecommerce}")
            print("Maaf, anda harus login terlebih dahulu.")

# library yang dibutuhkan
import random
import string
from datetime import datetime

# nama toko/app e-commerce
nama_ecommerce = 'BuyIt!'

# daftar nama database
db_user_account = 'database/user_account.txt'
db_produk = 'database/produk_jualbeli.txt'
db_keranjang = 'database/keranjang_belanja.txt'

if __name__ == "__main__":
    main()
