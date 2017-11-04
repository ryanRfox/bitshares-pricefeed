# Price Feed Script for BitShares

## Installation 

Ubuntu 16.04 LTS

Start the installation

```
cd ~
pip3 install bitshares-pricefeed --user
```

Create config.yml
```
bitshares-pricefeed create
```

Add a feed producer name to the config.yml file just created
```
vim config.yml
# The producer name(s)
producer: your_witness_name
```

Enter Credentials

```
uptick addkey
```

You will need to enter your cli wallet encryption passphrase here:

```
Wallet Encryption Passphrase:
Repeat for confirmation:
```

You will need to enter your Private Key (Active key) here. Hit enter the second time it asks you.

```
Private Key (wif) [Enter to quit]:
```

Manually run the feed update

```
bitshares-pricefeed update
```

Create a place for a logfile

```
sudo touch /var/log/bitshare-pricefeed.log
sudo chown ubuntu /var/log/bitshare-pricefeed.log
```

Add to cron, where PASSWD is your Wallet Encryption Passphrase

```
$ crontab -e

SHELL=/bin/bash
UNLOCK="PASSWD"

0,30 * * * * bitshares-pricefeed --configfile /home/ubuntu/config.yml --no-confirm-warning updat>> /var/log/bitshares-pricefeed.log 2>&1
```

## Help

```
# bitshares-pricefeed --help
Usage: bitshares-pricefeed [OPTIONS] COMMAND [ARGS]...

Options:
  --configfile TEXT
  --confirm-warning / --no-confirm-warning
                                  Need for manual confirmation of warnings
  --skip-critical / --no-skip-critical
                                  Skip critical feeds
  --help                          Show this message and exit.

Commands:
  create  Create config file
  update  Update price feed for assets
```

# IMPORTANT NOTE

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
